import logging

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from rest_framework.decorators import action
from core.business import BusinessNode
from core.enums import UpdateType
from core.helper.file_helper import SqlFileHelper
from core.helper.model_helper import get_value
from core.views.baseview import BaseModelApiView, BaseSqlApiView
from common.models.user_group import CmUser, CmGroup, CmRole
from common.serializers.user_group import CmUserSerializer, CmGroupSerializer, CmRoleSerializer

LOGGER = logging.getLogger(__name__)


# 사용자 목록
class UserListView(BaseModelApiView):
    """사용자 정보"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='user', model=CmUser, serializer=CmUserSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        filter_data = Q()
        if 'search_text' in request_data:
            filter_data.add(Q(user_id__contains=request_data.get('search_text'))
                            | Q(user_name__contains=request_data.get('search_text'))
                            | Q(email__contains=request_data.get('search_text'))
                            | Q(remark__contains=request_data.get('search_text')), Q.AND)
        return filter_data

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)


# 사용자 정보
class UserView(BaseModelApiView):
    """사용자 정보"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='user', model=CmUser, serializer=CmUserSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # url에 전달된 pk를 조회조건으로 설정
        return dict({'user_id': self.kwargs['user_id']})

    @action(detail=True, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)


# 그룹 목록
class GroupView(BaseModelApiView):
    """그룹 목록"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='group', model=CmGroup, serializer=CmGroupSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        filter_data = Q()
        if 'search_text' in request_data:
            filter_data.add(Q(group_name__contains=request_data.get('search_text'))
                            | Q(remark__contains=request_data.get('search_text')), Q.AND)
        return filter_data

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)


# Role 목록
class RoleView(BaseModelApiView):
    """Role 목록"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='role', model=CmRole, serializer=CmRoleSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        filter_data = Q()
        if 'search_text' in request_data:
            filter_data.add(Q(role_name__contains=request_data.get('search_text'))
                            | Q(remark__contains=request_data.get('search_text')), Q.AND)
        return filter_data

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)


# 사용자 정보
class UserDetailView(BaseSqlApiView):
    """사용자 정보"""

    # region 노드 정의

    def define_nodes(self):
        """비즈니스 로직 실행(조회/저장)에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # 사용자 정보 조회
        node_user_detail = BusinessNode()
        node_user_detail.node_name = 'user-detail'
        node_user_detail.sql_filename = 'user_detail'
        node_user_detail.table_name = 'cm_user'
        self._append_node(node_user_detail)

        # 사용자 정보 관리 조회
        node_user_info = BusinessNode()
        node_user_info.node_name = 'user-info'
        node_user_info.sql_filename = 'user_detail'
        node_user_info.model = CmUser
        node_user_info.table_name = 'cm_user'
        node_user_info.key_columns = ['user_id']
        node_user_info.update_columns = ['user_id', 'user_name', 'pwd', 'user_level', 'use_yn', 'emp_no', 'tel_no',
                                         'email', 'remark', 'first_rg_yms', 'first_rg_idf', 'last_update_yms',
                                         'last_update_idf']
        self._append_node(node_user_info)

        # 공사업체 사용자 정보 조회
        node_cust_user_detail = BusinessNode()
        node_cust_user_detail.node_name = 'cust-user-detail'
        node_cust_user_detail.sql_filename = 'cust_user_detail'
        node_cust_user_detail.table_name = 'cm_user'
        self._append_node(node_cust_user_detail)

    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # 조회조건을 추가하기 위해 오버라이딩
        filter_data = {}

        # 파라미터 설정
        user_id = ''
        if len(request_data) > 0 and 'p_user_id' in request_data:
            user_id = request_data.get('p_user_id')
        else:
            # 요청한 ID가 없으면 현재 사용자 정보 조회
            user_id = self.user_id

        filter_data = {
            'p_user_id': user_id,
        }

        return filter_data

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)

    # endregion

    # region 저장

    def _pre_update(self, node: BusinessNode, update_type: UpdateType, update_data: list, req_data) -> None:
        """변경된 데이터를 저장하기 전 호출되는 메서드입니다.
        사용자 생성시 초기 비밀번호를 설정합니다.
        """

        if update_type == UpdateType.Update:
            # Password 칼럼 추가 및 hashed 비밀번호 설정, 비밀번호 칼럼은 Backend에서만 사용(post_update에서 제거)
            for row in update_data:
                row['pwd'] = make_password(row['pwd'])
                # if row['pwd'] == row['new_pwd']:
                #     if row['new_pwd'] == row['new_pwd_chk']:
                #         row['pwd'] = make_password(row['pwd'])
                #         row['new_pwd'] = make_password(row['new_pwd'])
                #         row['new_pwd_chk'] = make_password(row['new_pwd_chk'])

    @action(detail=False, methods=['post'])
    def save(self, request):
        return self._exec_action(func=self._update_pwd, request=request)

    @action(detail=False, methods=['post'])
    def _update_pwd(self, req_data):
        row = req_data.get('cm_user')[0]
        user_id = row.get('user_id')
        pwd = row.get('pwd')
        pwd_new = row.get('pwd_new')
        key_data = {
            'user_id': user_id
        }

        if pwd_new is not None:
            db_password = get_value(model=CmUser, filter_data=key_data, column='pwd')
            if db_password is None:
                return '사용자 정보가 없습니다.'

            # 기존 비밀번호 확인
            if check_password(pwd, db_password):
                update_data = {
                        'pwd': make_password(pwd_new),
                        'email': row.get('email'),
                        'tel_no': row.get('tel_no')
                    }
                update_cm_user = CmUser.objects.filter(**key_data).update(**update_data)

            else:
                return 'false'

        else:
            update_data = {
                'email': row.get('email'),
                'tel_no': row.get('tel_no')
            }
            update_cm_user = CmUser.objects.filter(**key_data).update(**update_data)

        return req_data

    # endregion

