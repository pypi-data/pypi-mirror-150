import logging

from rest_framework.decorators import action
from core.business import BusinessNode
from core.helper.file_helper import SqlFileHelper
from core.views.baseview import BaseModelApiView, BaseSqlApiView
from core.helper.request_helper import get_corp_code_by_current_user

LOGGER = logging.getLogger(__name__)


class CmDashboardView(BaseSqlApiView):
    """대시보드 차트 #1 """

    # region 노드 정의

    def define_nodes(self):
        """비즈니스 로직 실행(조회/저장)에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # 대시보드 차트 #1
        node_chart1 = BusinessNode()
        node_chart1.node_name = 'chart1'
        node_chart1.sql_filename = 'dashboard_chart_first'
        node_chart1.table_name = 'sfty01020_chart'
        self._append_node(node_chart1)

        # 대시보드 차트 #3
        node_chart3 = BusinessNode()
        node_chart3.node_name = 'chart3'
        node_chart3.sql_filename = 'dashboard_chart_third'
        node_chart3.table_name = 'envt03040_chart'
        self._append_node(node_chart3)

    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # 조회조건을 추가하기 위해 오버라이딩
        filter_data = {}

        # 파라미터 추가 설정
        if node.node_name in ['chart1', 'chart3']:
            filter_data = {
                'p_corp_code': get_corp_code_by_current_user(),
                'p_ret_yy': request_data.get('p_ret_yy'),
            }

        filter_data.update(request_data)

        return filter_data

    @action(detail=False, methods=['post'])
    def get_chart1(self, request):
        """대시보드 차트 #1
        """
        return self._exec_get(request)

    @action(detail=False, methods=['post'])
    def get_chart3(self, request):
        """대시보드 차트 #3
        """
        return self._exec_get(request)

    # endregion
