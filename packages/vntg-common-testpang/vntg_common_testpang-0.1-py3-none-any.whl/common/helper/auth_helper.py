from datetime import datetime

from core.helper.file_helper import SqlFileHelper
from core.helper.model_helper import get_list, get_value
from core.helper.request_helper import get_current_user_id
from core.helper.sql_helper import get_list as get_list_by_sql

from common.models.authentication import CmUserRole, CmUserMenuAuth
from common.models.user_group import CmUser

# SqlFileHelper 등록
_sql_helper = SqlFileHelper(__package__)


def get_user_ids_in_role(role_no: str) -> list:
    """해당 Role번호에 속한 사용자ID 반환
    
    :param role_no: Role번호
    :return: 사용자ID 목록
    """
    result = get_list(model=CmUserRole, filter_data={'role_no': role_no}, columns=['user_id'])

    return result


def get_user_id_by_emp_no(emp_no: str) -> str:
    """사원번호에 해당하는 사용자ID 반환

    :param emp_no: 사원번호
    :return: 사용자ID
    """
    result = get_value(model=CmUser, filter_data={'emp_no': emp_no, 'user_level': '9'}, column='user_id')
    return result


def delete_menu_auth(user_id: str) -> int:
    """사용자 권한 메뉴 자료를 삭제합니다.

    :param user_id: 사용자ID
    :return: 삭제된 행 갯수
    """
    # 사용자 메뉴 정보 삭제
    affect_count = CmUserMenuAuth.objects.filter(**{'user_id': user_id}).delete()

    return affect_count


def select_menu_auth(user_id: str) -> list:
    """사용자 메뉴 목록을 조회합니다.

    :param user_id: 사용자ID
    :return: 사용자 메뉴 목록
    """
    db_rows = get_list(CmUserMenuAuth, filter_data={'user_id': user_id})

    return db_rows


def create_menu_auth(user_id: str):
    """사용자 권한 메뉴 자료를 생성합니다.
    그룹 권한 + 사용자 권한

    메뉴의 권한이 설정되는 곳에서 호출됩니다.
    - 그룹등록, 메뉴기준권한등록, 그룹기준권한등록, 사용자기준권한등록?

    :param user_id: 사용자ID
    """
    # 사용자 권한 메뉴 새롭게 설정하기 위해 기존 자료를 삭제합니다.
    delete_menu_auth(user_id)

    # 쿼리
    group_sql_query = _sql_helper.get_query('COMM_group_auth')
    user_sql_query = _sql_helper.get_query('COMM_user_auth')
    menu_sql_query = _sql_helper.get_query('COMM_menu')

    filter_data = {'user_id': user_id}
    # 그룹권한목록
    filter_data = dict((key if key.startswith('p_') else f'p_{key}', value) for key, value in filter_data.items())
    group_auth_list = get_list_by_sql(sql_query=group_sql_query, filter_data=filter_data)
    group_auth_dict = {}
    if group_auth_list is not None:
        group_auth_dict = {group_auth_row['menu_tree_sno']: group_auth_row for group_auth_row in group_auth_list}

    # 사용자권한목록
    user_auth_list = get_list_by_sql(sql_query=user_sql_query, filter_data=filter_data)

    # 그룹권한 + 개인권한 - 그룹권한과 개인권한에 동일한 메뉴가있으면 개인권한으로 갱신
    if user_auth_list is not None:
        user_auth_dict = {user_auth_row['menu_tree_sno']: user_auth_row for user_auth_row in user_auth_list}
        group_auth_dict.update(user_auth_dict)

    if group_auth_dict is None or len(group_auth_dict) == 0:
        # 권한받은 화면이 없음
        return

    # 메뉴 목록 - pgm_type : F(폴더)
    menu_list = get_list_by_sql(sql_query=menu_sql_query, filter_data=filter_data)
    # 프로그램 목록 - pgm_type : F(폴더) 외
    pgm_auth_list = [value for key, value in group_auth_dict.items()]

    for pgm_auth_row in pgm_auth_list:
        # 사용자 권한이 있는 메뉴만 프로그램 목록에 추가
        filter_auth_menu(menu_list, pgm_auth_list, pgm_auth_row)

    # 토큰이 있으면(일반사용자) 사용자 계정 정보, 없으면(공사업체) 권한 부여 사용자 계정으로 설정
    try:
        user_id = get_current_user_id()
    except Exception as ex:
        pass

    bulk_list = []
    for pgm_auth_row in pgm_auth_list:
        pgm_auth_row.update({'first_rg_yms': datetime.now()})
        pgm_auth_row.update({'first_rg_idf': user_id})
        pgm_auth_row.update({'last_update_yms': datetime.now()})
        pgm_auth_row.update({'last_update_idf': user_id})
        # affect_count = CmUserMenuAuth.objects.create(**pgm_auth_row)
        bulk_list.append(CmUserMenuAuth(**pgm_auth_row))

    # 테이블 저장 (Model을 이용하고, connection을 줄이기 위해 bulk_create 사용)
    CmUserMenuAuth.objects.bulk_create(bulk_list)


def filter_auth_menu(menu_list, pgm_auth_list, pgm_auth_row):
    """메뉴 목록에서 해당 프로그램의 부모 메뉴 일련번호로 상위 메뉴 일련번호 찾기
    """
    parent_menu_list = [menu_data for menu_data in menu_list
                        if menu_data['menu_tree_sno'] == pgm_auth_row['parent_menu_tree_sno']]

    if parent_menu_list:
        # 발견된 부모 메뉴
        parent_menu_row = parent_menu_list[0]

        # 프로그램 목록에 메뉴 일련번호가 이미 존재하면 Skip 없으면 추가
        if bool([row for row in pgm_auth_list if row['menu_tree_sno'] == parent_menu_row['menu_tree_sno']]):
            pass
        else:
            # 프로그램 목록에 해당 프로그램에 대한 상위 메뉴 추가
            pgm_auth_list.append(parent_menu_row)
            # 상위 메뉴 추가
            filter_auth_menu(menu_list, pgm_auth_list, parent_menu_row)
