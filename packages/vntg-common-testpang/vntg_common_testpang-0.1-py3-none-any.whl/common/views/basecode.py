import logging

from django.db.models import Q
from rest_framework import permissions
from rest_framework.decorators import action

from core.business import BusinessNode
from core.helper.file_helper import SqlFileHelper
from core.views.baseview import BaseModelApiView, BaseSqlApiView
from common.models.basecode import CmCodeMaster, CmCodeDetail
from common.serializers.basecode import CmCodeMasterSerializer, CmCodeDetailSerializer

LOGGER = logging.getLogger(__name__)


class CodeMasterView(BaseModelApiView):
    """공통코드 코드유형 정보 조회"""

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='code', model=CmCodeMaster, serializer=CmCodeMasterSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # url에 전달된 pk를 조회조건으로 설정
        return dict({'cm_code_type_id': self.kwargs['cm_code_type_id']})

    @action(detail=True, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)


class CodeDetailView(BaseModelApiView):
    """공통코드 리스트 조회"""

    def define_nodes(self):
        # 리스트 노드 등록
        self._append_node(BusinessNode(node_name='list', model=CmCodeDetail, serializer=CmCodeDetailSerializer))
        # 디테일 노드 등록
        self._append_node(BusinessNode(node_name='detail', model=CmCodeDetail, serializer=CmCodeDetailSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # url에 전달된 pk를 조회조건으로 설정
        if node.node_name == 'list':
            # Q를 이용하여 파라미터 설정
            filter_data = Q()
            # cm_code_type_id는 작성된 endpoint로 고정
            filter_data.add((Q(cm_code_type_id=self.kwargs['cm_code_type_id'])), Q.AND)
            # 사용여부 'Y'일 때 미사용 포함
            if 'use_yn' in request_data and request_data.get('use_yn') == 'Y':
                pass
            else:
                filter_data.add(Q(use_yn='Y'), Q.AND)
            if 'search_text' in request_data:
                filter_data.add((Q(detail_code_id__contains=request_data.get('search_text'))
                                 | Q(detail_code_name__contains=request_data.get('search_text'))), Q.AND)
            if 'etc_ctnt' in request_data and request_data.get('etc_ctnt') != '%':
                filter_data.add((Q(etc_ctnt1__contains=request_data.get('etc_ctnt'))
                                 | Q(etc_ctnt2__contains=request_data.get('etc_ctnt'))
                                 | Q(etc_ctnt3__contains=request_data.get('etc_ctnt'))
                                 | Q(etc_ctnt4__contains=request_data.get('etc_ctnt'))
                                 | Q(etc_ctnt5__contains=request_data.get('etc_ctnt'))), Q.AND)
            if 'etc_ctnt1' in request_data and request_data.get('etc_ctnt1') != '%':
                filter_data.add(Q(etc_ctnt1=request_data.get('etc_ctnt1')), Q.AND)
            if 'etc_ctnt2' in request_data and request_data.get('etc_ctnt2') != '%':
                filter_data.add(Q(etc_ctnt2=request_data.get('etc_ctnt2')), Q.AND)
            if 'etc_ctnt3' in request_data and request_data.get('etc_ctnt3') != '%':
                filter_data.add(Q(etc_ctnt3=request_data.get('etc_ctnt3')), Q.AND)
            if 'etc_ctnt4' in request_data and request_data.get('etc_ctnt4') != '%':
                filter_data.add(Q(etc_ctnt4=request_data.get('etc_ctnt4')), Q.AND)
            if 'etc_ctnt5' in request_data and request_data.get('etc_ctnt5') != '%':
                filter_data.add(Q(etc_ctnt5=request_data.get('etc_ctnt5')), Q.AND)

            return filter_data
        elif node.node_name == 'detail':
            # return dict({'cm_code_type_id': self.kwargs['cm_code_type_id'],
            #              'detail_code_id': self.kwargs['detail_code_id']
            #              })
            return super()._create_filter(node=node, parameter_list=parameter_list, request_data=request_data,
                                          include_all=include_all)
        else:
            return None

    @action(detail=False, methods=['post'])
    def get_list(self, request, *args, **kwargs):
        return self._exec_get(request)

    @action(detail=True, methods=['post'])
    def get_detail(self, request, *args, **kwargs):
        return self._exec_get(request)


class CodeListView(BaseSqlApiView):
    """공통코드 전체 리스트 조회

    [Parameters]
    - cm_code_type_id: 공통코드유형 식별자
    - search_text: 검색어(공통코드유형명, 코드명)
    """
    permission_classes = (permissions.AllowAny,)

    def define_nodes(self):
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # 코드리스트
        node_codelist = BusinessNode()
        node_codelist.node_name = 'codelist'
        node_codelist.sql_filename = 'CodeListView'
        node_codelist.table_name = 'codelist'
        node_codelist.key_columns = ['cm_code_type_id', 'detail_code_id']
        self._append_node(node_codelist)

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # 파라미터 설정
        filter_data = {'p_cm_code_type_id': request_data.get('cm_code_type_id', '%'),
                       'p_search_text': request_data.get('search_text', '%'),
                       }
        return filter_data

    def _get_list(self, node: BusinessNode):
        """
        기준코드 전체 리스트를 code_type -> code_type 정보 -> codedetail (list) 형태로 변환
        """
        basecode_list = super()._get_list(node)

        # code_type_id 만 unique하게 추출
        code_type_list = set(item['cm_code_type_id'] for item in basecode_list)

        serialized_data = {}
        for code_type in code_type_list:
            # code_type 정보 1건 검색
            row = next((item for item in basecode_list if item['cm_code_type_id'] == code_type), None)

            # code_type 정보 설정
            serialized_data[code_type] = {
                'cm_code_type_id': code_type,
                'cm_code_type_name': row['cm_code_type_name'],
                'parent_code_type_id': row['parent_code_type_id'],
                'cm_code_length': row['cm_code_length'],
                'system_yn': row['system_yn'],
                'codedetail': []
            }

            # code_type에 대한 code list 등록
            serialized_data[code_type]['codedetail'] = list(
                filter(lambda x: x['cm_code_type_id'] == code_type, basecode_list))

            # code list에서 불필요한 칼럼 제거
            for detail_row in serialized_data[code_type]['codedetail']:
                detail_row.pop('cm_code_type_name')
                detail_row.pop('parent_code_type_id')
                detail_row.pop('cm_code_length')
                detail_row.pop('system_yn')
                detail_row.pop('row_stat')

        return serialized_data

    @action(detail=False, methods=['post'])
    def get_list(self, request, *args, **kwargs):
        return self._exec_get(request)
