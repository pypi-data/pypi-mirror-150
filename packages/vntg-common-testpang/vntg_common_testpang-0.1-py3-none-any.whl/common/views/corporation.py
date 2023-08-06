import logging

from rest_framework.decorators import action

from core.business import BusinessNode
from core.helper.request_helper import get_corp_code_by_current_user
from core.views.baseview import BaseModelApiView

from common.models.corporation import CmCorporation, CmBusiplace
from common.serializers.corporation import CmCorporationSerializer, CmBusiplaceSerializer

LOGGER = logging.getLogger(__name__)


class CmCorporationView(BaseModelApiView):
    """법인 목록"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='corporation', model=CmCorporation, serializer=CmCorporationSerializer))

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)


class CmBusiplaceView(BaseModelApiView):
    """사업장 목록"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='busi-place', model=CmBusiplace, serializer=CmBusiplaceSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # 조회조건을 추가하기 위해 오버라이딩
        if node.node_name == 'busi-place':
            filter_data = {
                'corp_code': get_corp_code_by_current_user(),
            }
            # 불필요한 파라미터 제거
            filter_data = {key: value for key, value in filter_data.items() if value is not None and value != '%'}
            # 하위 테이블 조건 유무 확인
            if len(filter_data) == 0:
                raise Exception('조회 조건이 누락되었습니다.')
            return filter_data

    def _set_query(self, node: BusinessNode, request_data: dict):
        if node.node_name == 'busi-place':
            filter_data = self._create_filter(node=node, parameter_list=None, request_data=request_data,
                                              include_all=False)

            # Group 이름을 extra()로 조인 조회 - 모델에 foreign key가 설정되어 있지 않은 경우.
            # extra()의 select/tables/where는 실제 query(select/from/where)에 반영된다.
            # URL에서 받은 법인 pk를 이용하여 해당 법인에 속한 사업장을 조회한다.
            node.queryset = node.model.objects.extra(
                select={'corp_name': 'cm_corporation.corp_name'},
                tables=['cm_corporation'],
                where=['cm_corporation.corp_code=cm_busiplace.corp_code']
            ).filter(**filter_data)

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)
