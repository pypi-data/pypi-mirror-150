import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.helper.auth_helper import create_menu_auth
from core.business import BusinessNode
from core.helper import get_node_name_by_path
from core.helper.file_helper import SqlFileHelper
from core.helper.request_helper import get_current_user_id
from core.views.baseview import BaseModelApiView, BaseSqlApiView

from common.models.authentication import CmGroupUsers, CmUserRole
from common.serializers.authentication import CmUserGroupSerializer, CmGroupUsersSerializer, CmUserRoleSerializer

LOGGER = logging.getLogger(__name__)


# 그룹에 속한 사용자 목록
class GroupUsersView(BaseModelApiView):
    """그룹에 속한 사용자 목록"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='users', model=CmGroupUsers, serializer=CmGroupUsersSerializer))

    def _set_query(self, node, request_data: dict):
        filter_data = self._create_filter(node=node, parameter_list=None, request_data=request_data, include_all=False)

        # 사용자이름을 extra()로 조인 조회 - 모델에 foreign key가 설정되어 있지 않은 경우.
        # extra()의 select/tables/where는 실제 query(select/from/where)에 반영된다.
        # URL에서 받은 그룹 pk를 이용하여 해당 그룹에 속한 사용자를 조회한다.
        node.queryset = node.model.objects.extra(
            select={'user_name': 'cm_user.user_name'},
            tables=['cm_user'],
            where=['cm_user.user_id=cm_group_users.user_id']
        ).filter(filter_data)

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)


# 사용자가 해당 그룹이나 롤에 속하는지 체크
class UserGroupRoleCheckView(BaseModelApiView):
    """사용자가 해당 그룹이나 롤에 속하는지 체크"""

    def define_nodes(self):
        pass

    @action(detail=True, methods=['post'])
    def check_group(self, request, *args, **kwargs):
        # key 조건으로 테이블 검색
        db_row = self._get_object(model=CmGroupUsers, pk_data=self.kwargs)

        if db_row is None:
            return Response({'success': True, 'code': 0, 'message': '해당 그룹에 소속되지 않습니다.', 'data': False},
                            status.HTTP_200_OK)
        else:
            return Response({'success': True, 'code': 1, 'message': 'OK', 'data': True},
                            status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def check_role(self, request, *args, **kwargs):
        # key 조건으로 테이블 검색
        db_row = self._get_object(model=CmUserRole, pk_data=self.kwargs)

        if db_row is None:
            return Response({'success': True, 'code': 0, 'message': '해당 Role을 갖고있지 않습니다.', 'data': False},
                            status.HTTP_200_OK)
        else:
            return Response({'success': True, 'code': 1, 'message': 'OK', 'data': True},
                            status.HTTP_200_OK)


# 사용자의 그룹 목록
class UserGroupView(BaseModelApiView):
    """사용자의 그룹 목록"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='group', model=CmGroupUsers, serializer=CmUserGroupSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        filter_data = Q()

        # user_id가 없으면 현재 사용자 정보 사용
        if 'user_id' in request_data:
            user_id = request_data.get('user_id')
        else:
            user_id = get_current_user_id()

        filter_data.add(Q(user_id=user_id), Q.AND)
        return filter_data

    def _set_query(self, node, request_data: dict):
        filter_data = self._create_filter(node=node, parameter_list=None, request_data=request_data, include_all=False)

        # 그룹이름을 extra() subquery로 조회 - 모델에 foreign key가 설정되어 있지 않은 경우.
        # extra()의 select/tables/where는 실제 query(select/from/where)에 반영된다.
        # URL에서 받은 그룹 pk를 이용하여 해당 그룹에 속한 사용자를 조회한다.
        node.queryset = node.model.objects.extra(
            select={'group_name': 'cm_group.group_name',
                    'system_type': 'cm_group.system_type',
                    'use_yn': 'cm_group.use_yn',
                    'remark': 'cm_group.remark'},
            tables=['cm_group'],
            where=['cm_group_users.group_sno=cm_group.group_sno']
        ).filter(filter_data)

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        """지정한 사용자가 속한 그룹 목록

        요청파라미터
        - user_id: 사용자id, 생략가능
        """
        return self._exec_get(request)


# 사용자의 롤 목록
class UserRoleView(BaseModelApiView):
    """사용자의 롤 목록"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='role', model=CmUserRole, serializer=CmUserRoleSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        filter_data = Q()

        # user_id가 없으면 현재 사용자 정보 사용
        if 'user_id' in request_data:
            user_id = request_data.get('user_id')
        else:
            user_id = get_current_user_id()

        filter_data.add(Q(user_id=user_id), Q.AND)

        # 롤 일련번호 endpoint로 호출된 경우 filter_data에 role_no 추가
        if len(self.kwargs) > 0:
            filter_data.add(Q(role_no=self.kwargs['role_no']), Q.AND)
        return filter_data

    def _set_query(self, node, request_data: dict):
        filter_data = self._create_filter(node=node, parameter_list=None, request_data=request_data, include_all=False)

        # 사용자이름을 extra()로 조인 조회 - 모델에 foreign key가 설정되어 있지 않은 경우.
        # extra()의 select/tables/where는 실제 query(select/from/where)에 반영된다.
        # URL에서 받은 그룹 pk를 이용하여 해당 그룹에 속한 사용자를 조회한다.
        node.queryset = node.model.objects.extra(
            select={'role_name': 'cm_role.role_name',
                    'role_type': 'cm_role.role_type',
                    'system_yn': 'cm_role.system_yn',
                    'use_yn': 'cm_role.use_yn',
                    'remark': 'cm_role.remark'},
            tables=['cm_role'],
            where=['cm_user_role.role_no=cm_role.role_no']
        ).filter(filter_data)

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        """지정한 사용자가 소유한 롤 목록

        요청파라미터
        - user_id: 사용자id, 생략가능
        """
        return self._exec_get(request)

    @action(detail=False, methods=['post'])
    def get_auth_role(self, request, *args, **kwargs):

        # request path를 이용하여 노드 검색
        node_name = get_node_name_by_path(request.path)

        # 조회
        serialized_data = self.get_list_by_node_name(node_name=node_name, parameters=request.data)

        if len(serialized_data) == 0:
            return Response({'success': True, 'code': 0, 'message': '해당 Role을 갖고있지 않습니다.', 'data': False},
                            status.HTTP_200_OK)
        else:
            # Role 명
            role_name = serialized_data[0].get('role_name')

            return Response({'success': True, 'code': 1, 'message': f'role 명: {role_name}', 'data': True},
                            status.HTTP_200_OK)


# 사용자의 메뉴 목록
class UserMenuView(BaseSqlApiView):
    """사용자의 메뉴 목록"""

    # region 노드 정의

    def define_nodes(self):
        """비즈니스 로직 실행(조회/저장)에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # 메뉴
        node_menu_auth = BusinessNode()
        node_menu_auth.node_name = 'menu'
        node_menu_auth.sql_filename = 'auth_menu'
        node_menu_auth.table_name = 'menu_list'
        self._append_node(node_menu_auth)

    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):

        # user_id가 없으면 현재 사용자 정보 사용
        if 'p_user_id' in request_data:
            user_id = request_data.get('p_user_id')
        else:
            user_id = get_current_user_id()
        # 파라미터 설정
        filter_data = {
            'p_user_id': user_id,
            # 실행일련번호가 endpoint로 호출된 경우를 위해 추가
            'p_run_sno': '%',
        }

        # 실행 일련번호 endpoint로 호출된 경우 filter_data에 run_sno 추가
        if len(self.kwargs) > 0:
            filter_data.update({'p_run_sno': str(self.kwargs['run_sno'])})

        return filter_data

    # def _get_list(self, node: BusinessNode):
    #     """node에 설정된 query를 이용하여 데이터 조회하고, 결과를 반환합니다.
    #
    #     :param node: 조회를 실행하고자 하는 노드
    #     :return: 조회 결과(행 리스트)
    #     """
    #     if node.node_name == 'menu':
    #         # 노드에 설정된 query 조회 - 그룹메뉴권한 + 개인메뉴권한 + 메뉴
    #         serialized_data = super()._get_list(node=node)
    #
    #         # 메뉴 목록 - pgm_type : F(폴더)
    #         menu_list = [row for row in serialized_data if row['pgm_type'] == 'F']
    #         # 프로그램 목록 - pgm_type : F(폴더) 외
    #         pgm_auth_list = [row for row in serialized_data if row['pgm_type'] != 'F']
    #
    #         for pgm_auth_row in pgm_auth_list:
    #             # 사용자 권한이 있는 메뉴만 프로그램 목록에 추가
    #             self.filter_auth_menu(menu_list, pgm_auth_list, pgm_auth_row)
    #
    #         return pgm_auth_list
    #     else:
    #         return super()._get_list(node=node)
    #
    # def filter_auth_menu(self, menu_list, pgm_list, pgm_auth_row):
    #     # 메뉴 목록에서 해당 프로그램의 부모 메뉴 일련번호로 상위 메뉴 일련번호 찾기
    #     parent_menu_list = [menu_data for menu_data in menu_list
    #                         if menu_data['menu_tree_sno'] == pgm_auth_row['parent_menu_tree_sno']]
    #
    #     if parent_menu_list:
    #         # 발견된 부모 메뉴
    #         parent_menu_row = parent_menu_list[0]
    #
    #         # 프로그램 목록에 메뉴 일련번호가 이미 존재하면 Skip 없으면 추가
    #         if bool([row for row in pgm_list if row['menu_tree_sno'] == parent_menu_row['menu_tree_sno']]):
    #             pass
    #         else:
    #             # 프로그램 목록에 해당 프로그램에 대한 상위 메뉴 추가
    #             pgm_list.append(parent_menu_row)
    #             # 상위 메뉴 추가
    #             self.filter_auth_menu(menu_list, pgm_list, parent_menu_row)

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        """사용자별 메뉴+프로그램 권한 목록 조회

        요청 파라미터
        - user_id: 사용자id, 생략가능
        """
        return self._exec_get(request)

    @action(detail=False, methods=['post'])
    def get_auth_menu(self, request, *args, **kwargs):

        # request path를 이용하여 노드 검색
        node_name = get_node_name_by_path(request.path)

        # 조회
        serialized_data = self.get_list_by_node_name(node_name=node_name, parameters=request.data)

        if len(serialized_data) == 0:
            return Response({'success': True, 'code': 0, 'message': '해당 Menu를 갖고있지 않습니다.', 'data': 'N/N/N'},
                            status.HTTP_200_OK)
        else:
            # Menu 명, 조회/출력/수정
            menu_name = serialized_data[0].get('menu_name')
            select_yn = serialized_data[0].get('select_yn')
            print_yn = serialized_data[0].get('print_yn')
            save_yn = serialized_data[0].get('save_yn')

            return Response({'success': True, 'code': 1, 'message': f'menu 명: {menu_name}',
                             'data': f'{select_yn}/{print_yn}/{save_yn}'}, status.HTTP_200_OK)

    # endregion


# 사용자 메뉴 생성
class UserMenuAuthCreateView(BaseModelApiView):
    """사용자 권한 메뉴 자료를 생성합니다.
    그룹 권한 + 사용자 권한
    """
    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='create'))

    @action(detail=False, methods=['post'])
    def save(self, request):
        """사용자 권한 메뉴 자료를 생성

        요청 파라미터
        - user_ids: 사용자id, 사용자 아이디가 여러개일 경우 콤마(,) 구분자로 나열
        """
        try:
            user_ids = request.data['user_ids'].replace(' ', '').split(',')

            for user_id in user_ids:
                # 사용자 메뉴 권한을 생성합니다.
                create_menu_auth(user_id)
            return Response({'success': True, 'code': 1, 'message': '사용자 메뉴 권한을 설정하였습니다.', 'data': True},
                            status.HTTP_200_OK)
        except Exception as ex:
            return Response({'success': True, 'code': 0, 'message': f'사용자 메뉴 권한을 설정에 실패하였습니다. 오류메세지 : {str(ex)}', 'data': False},
                            status.HTTP_200_OK)
