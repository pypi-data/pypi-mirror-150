from core.helper import sql_helper, model_helper
from core.helper.file_helper import SqlFileHelper
from core.helper.request_helper import get_corp_code_by_current_user, get_busi_place_by_current_user

from common.models.corporation import CmBusiplace
from common.models.employee import CmDepartment, CmEmployee
from common.models.user_group import CmUser

# SqlFileHelper 등록
_sql_helper = SqlFileHelper(__package__)

"""
    법인, 사업장, 부서, 사원정보 조회 helper

    Usage:
        from common.helper import organizationhelper
        
        organizationhelper.get_busiplace_list(['corp_code', 'busi_place'])
"""

# region 법인 정보

# endregion

# region 사업장 정보


def get_busiplace_list(columns: list = None) -> list:
    """로그인 사용자의 법인에 소속된 사업장 목록을 조회합니다.

    :param columns: 조회하고자 하는 컬럼들
    """
    # 쿼리
    sql_query = _sql_helper.get_query('busiplace')

    # 조회조건
    filter_data = {
        # 법인코드: 토큰 정보에서 가져온 corp_code로 설정하기
        'p_corp_code': get_corp_code_by_current_user(),
        'p_busi_place': '%',
    }
    # 조회
    result_list = sql_helper.get_list(sql_query, filter_data=filter_data, columns=columns)
    return result_list


def get_busiplace_row(busi_place: str, columns: list = None) -> list:
    """로그인 사용자의 법인에 소속된 사업장 목록을 조회합니다.

    :param busi_place: 사업장코드
    :param columns: 조회하고자 하는 컬럼들
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'busi_place': busi_place,
    }
    # 조회
    result_row = model_helper.get_row(model=CmBusiplace, filter_data=filter_data, columns=columns)
    return result_row


def get_busiplace_name(busi_place: str) -> str:
    """사업장코드로 사업장 단축코드 조회합니다.

    :param busi_place: 사업장코드
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'busi_place': busi_place,
    }
    # 조회
    result_value = model_helper.get_value(model=CmBusiplace, filter_data=filter_data, column='busi_place_name')
    return result_value


def get_busiplace_shrt(busi_place: str) -> str:
    """사업장코드로 사업장 단축코드 조회합니다.

    :param busi_place: 사업장코드(예: 1000)
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'busi_place': busi_place
    }
    # 조회
    result_value = model_helper.get_value(model=CmBusiplace, filter_data=filter_data, column='busi_place_sht_name')
    return result_value


def get_busiplace_by_shrt(busi_place: str) -> str:
    """사업장 단축코드로 사업장코드를 조회합니다.

    :param busi_place: 사업장코드(예: P)
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'busi_place_sht_name': busi_place
    }
    # 조회
    result_value = model_helper.get_value(model=CmBusiplace, filter_data=filter_data, column='busi_place')
    return result_value

# endregion

# region 부서정보


def get_dept_list(busi_place: str = None, parent_dept_code: str = None) -> list:
    """부서 목록을 조회합니다.

    :param busi_place: 사업장코드
    :param parent_dept_code: 상위부서코드
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'busi_place': busi_place,
        'parent_dept_code': parent_dept_code,
    }
    # 조회조건 키의 값이 없으면 제거
    for key_column in [key for key, value in filter_data.items() if value is None]:
        filter_data.pop(key_column)

    # 조회
    result_list = model_helper.get_list(model=CmDepartment, filter_data=filter_data, columns=None)
    return result_list


def get_dept_row(dept_code: str) -> list:
    """부서코드로 부서명을 조회합니다.

    :param dept_code: 부서코드
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'dept_code': dept_code,
    }
    # 조회
    result_row = model_helper.get_row(model=CmDepartment, filter_data=filter_data, columns=None)
    return result_row


def get_dept_name(dept_code: str) -> str:
    """부서코드로 부서명을 조회합니다.

    :param dept_code: 부서코드
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'dept_code': dept_code,
    }
    # 조회
    result_value = model_helper.get_value(model=CmDepartment, filter_data=filter_data, column='dept_name')
    return result_value


def get_plant_code_by_emp_no(emp_no: str) -> str:
    """사원번호로 공장(부서) 행 정보를 조회합니다.

    :param emp_no: 사원번호
    """
    # 쿼리
    sql_query = _sql_helper.get_query('employee')

# 조회조건
    filter_data = {
        # 법인코드: 토큰 정보에서 가져온 corp_code로 설정
        'p_corp_code': get_corp_code_by_current_user(),
        # 'p_busi_place': get_busi_place_by_current_user(),
        'p_emp_no': emp_no,
    }
    # 조회
    result_value = sql_helper.get_value(sql_query, filter_data=filter_data, column='plant_code')
    # ToDO: 부서정보를 찾지 못한 경우 아스테리크 처리
    result_value = '*' if result_value is None else result_value

    return result_value

# endregion

# region 사원정보


def get_emp_list(busi_place: str = None, plant_code: str = None) -> list:
    """사원정보 목록을 조회합니다.

    :param busi_place: 사업장코드
    :param plant_code: 부서코드
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'busi_place': busi_place,
        'plant_code': plant_code,
    }
    # 조회조건 키의 값이 없으면 제거
    for key_column in [key for key, value in filter_data.items() if value is None]:
        filter_data.pop(key_column)

    # 조회
    result_list = model_helper.get_list(model=CmEmployee, filter_data=filter_data, columns=None)
    return result_list


def get_emp_name(emp_no: str) -> str:
    """사원 이름을 조회합니다.

    :param emp_no: 사원번호
    """
    # 조회조건
    filter_data = {
        'corp_code': get_corp_code_by_current_user(),
        'emp_no': emp_no,
    }
    # 조회
    result_value = model_helper.get_value(model=CmEmployee, filter_data=filter_data, column='emp_name')
    return result_value


def get_emp_no_by_user_id(user_id: str) -> str:
    """사용자ID로 사원번호를 조회합니다.

    :param user_id: 사용자ID
    """
    # 조회
    result_value = model_helper.get_value(model=CmUser, filter_data={'user_id': user_id}, column='emp_no')
    result_value = '*' if result_value is None else result_value

    return result_value

# endregion
