import logging

from rest_framework.decorators import action

from core.business import BusinessNode
from core.helper.file_helper import SqlFileHelper
from core.views.baseview import BaseSqlApiView

LOGGER = logging.getLogger(__name__)


class UserMainMenuView(BaseSqlApiView):
    """메뉴+프로그램+파라미터 목록"""

    # region 노드 정의

    def define_nodes(self):
        """비즈니스 로직 실행(조회/저장)에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # 메뉴 노드 등록
        self._append_node(BusinessNode(node_name='main-menu', sql_filename='MenuTreeView'))

    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        if request_data is None or len(request_data) == 0:
            # 요청 파라미터가 없으면 기본 파라미터 값 설정
            return dict({'p_system_type': '%'})
        else:
            # 파라미터명 변환 - system_code -> p_system_code
            return super()._create_filter(node, parameter_list, request_data, include_all)

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)

    # endregion


class UserMyMenuView(BaseSqlApiView):
    """사용자 My 메뉴"""

    # region 노드 정의

    def define_nodes(self):
        """사용자 개인 메뉴 조회에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # 개인 메뉴 목록 조회 - 마스터
        node_user_menu = BusinessNode()
        node_user_menu.node_name = 'user-menu'
        node_user_menu.sql_filename = 'UserMyMenuView'
        node_user_menu.table_name = 'search_data'

        self._append_node(node_user_menu)
    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # 조회조건을 추가하기 위해 오버라이딩
        filter_data = {}
        if node.node_name == 'user-menu':
            filter_data = {
                'p_user_id': request_data.get('p_user_id'),
            }

        return filter_data

    @action(detail=False, methods=['post'])
    def get_user_my_menu(self, request):
        """사용자 My 메뉴 리스트 조회

        요청 파라미터
        - user_id: 사용자 id, 필수
        """

        return self._exec_get(request)
    # endregion


class ProgramView(BaseSqlApiView):
    """프로그램 목록"""

    # region 노드 정의

    def define_nodes(self):
        """비즈니스 로직 실행(조회/저장)에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # 노드 등록
        self._append_node(BusinessNode(node_name='program', sql_filename='ProgramView'))

    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        filter_data = {'p_system_code': request_data.get('p_system_code', '%'),
                       'p_search_text': request_data.get('p_search_text', '%')}
        return filter_data

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         Parameter(name='system_code', in_=openapi.IN_BODY, type=openapi.TYPE_STRING, description='시스템 코드'),
    #         Parameter(name='search_text', in_=openapi.IN_BODY, type=openapi.TYPE_STRING, description='프로그램 ID,이름'),
    #     ]
    # )
    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)

    # endregion
