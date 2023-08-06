"""코드 참고 용
"""
import logging

from django.db import transaction
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView, Response

from common.serializers.test_serializers import *

LOGGER = logging.getLogger(__name__)


# 멀티 레코드를 업데이트하기 위한 테스트뷰
# APIView는 CBV(Class-based Views)이고 이를 사용하는 경우, Http 메서드에 해당하는 함수를 만들어줘야 함
# APIView를 아래처럼 작성하며, swagger ui에 request/response 스크마가 보이지 않음
class CmListView(APIView):
    serializer_class = CmCodeMasterListSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        # 조회 파라미터를 생성할 Dict 객체 생성
        filter_list = {'delete_yn': 'N'}

        # request body에 조회 조건을 확인하여 적용
        if len(self.request.data) > 0:
            # request.data 의 내용을 filter_list로 변환할 함수 필요(파라미터 값이 '%' 체크 필요)
            if self.request.data['system_yn'] != '%':
                filter_list['system_yn'] = 'Y'

        # 파라미터를 쿼리셋에 적용
        queryset = CmCodeMaster.objects.filter(**filter_list)

        LOGGER.debug(queryset.query)
        return queryset

    def get(self, request):
        """기준코드 리스트 조회"""
        serialized = self.serializer_class(self.get_queryset(), many=True)
        # Django가 아닌, DRF의 Response를 사용해야 함
        return_data = {"master": serialized.data}
        return Response(return_data)

    def post(self, request):
        """기준코드 리스트 저장
        row_stat 확인하여 처리 - added(Insert)/modified(Update)/deleted(Delete)"""
        # list(filter(lambda x: x['row_stat'] == 'added', request.data))
        request_data = request.data
        # serialized = self.serializer_class(data=request_data, many=isinstance(request_data, list))
        # raise_exception=True 이면, 이미 등록된 key의 경우 예외 발생-update 할 수 없음
        # serialized.is_valid(raise_exception=True)
        # serialized.is_valid()

        # Delete
        # self._perform_delete(request.data)
        # Update
        # self._perform_update(request.data)
        # Insert
        # self._perform_insert(request.data)

        modified_data = list(filter(lambda x: x['row_stat'] == 'modified', request_data))
        serialized = self.serializer_class(data=modified_data, many=isinstance(modified_data, list))
        self.request.method = 'PATCH'
        if serialized.is_valid():
            serialized.save()

        return Response(serialized.data)

    def _perform_delete(self, request_data):
        deleted_data = list(filter(lambda x: x['row_stat'] == 'deleted', request_data))
        serialized = self.serializer_class(data=deleted_data, many=isinstance(deleted_data, list))
        serialized.is_valid()
        serialized.validated_data

    def _perform_insert(self, request_data):
        added_data = list(filter(lambda x: x['row_stat'] == 'added', request_data))
        serialized = self.serializer_class(data=added_data, many=isinstance(added_data, list))
        if serialized.is_valid():
            serialized.save()
            return serialized.data

    def _perform_update(self, request_data):
        modified_data = list(filter(lambda x: x['row_stat'] == 'modified', request_data))
        serialized = self.serializer_class(data=modified_data, many=isinstance(modified_data, list))
        if serialized.is_valid():
            serialized.save()
            return serialized.data


class CmTestListViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    # router설정을 위해 주 모델을 queryset으로 설정 -> 현재 ViewSet에서는 사용하지 않음.
    queryset = CmCodeMaster.objects.all()

    def get_queryset(self):
        # 조회 파라미터를 생성할 Dict 객체 생성
        filter_list = {'delete_yn': 'N'}

        # request body에 조회 조건을 확인하여 적용
        if len(self.request.data) > 0:
            # request.data 의 내용을 filter_list로 변환할 함수 필요(파라미터 값이 '%' 체크 필요)
            if self.request.data['system_yn'] != '%':
                filter_list['system_yn'] = self.request.data['system_yn']

        # 파라미터를 쿼리셋에 적용
        queryset = CmCodeMaster.objects.filter(**filter_list)

        LOGGER.debug(queryset.query)
        return queryset

    def _list(self, request):
        LOGGER.debug('request - list')
        queryset = CmCodeMaster.objects.all()
        serializer = CmCodeMasterListSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(method='get', responses={200: CmCodeMasterListSerializer(many=True)},
                         operation_description='기준코드 마스터 조회')
    @action(detail=False, methods=['get'])
    def code_master(self, request):
        LOGGER.debug('request - get - code_master')
        # 마스터데이터는 get_queryset()을 이용해봄
        queryset = self.get_queryset()
        serializer = CmCodeMasterListSerializer(queryset, many=True)
        return_data = {"data": serializer.data}
        # Django가 아닌, DRF의 Response를 사용해야 함
        return Response(return_data)

    @swagger_auto_schema(method='get', responses={200: CmCodeDetailListSerializer(many=True)},
                         operation_description='기준코드 디테일 조회')
    @action(detail=False, methods=['get'])
    def code_detail(self, request):
        LOGGER.debug('request - get - code_detail')
        if len(self.request.data) == 0 or 'cm_code_type_id' not in self.request.data:
            return Response({'success': 'false', 'code': -1, 'message': 'cm_code_type_id이(가) 누락되었습니다.', 'data': None},
                            status=status.HTTP_400_BAD_REQUEST)

        # 조회 파라미터를 생성할 Dict 객체 생성 - request body에 조회 조건을 확인하여 적용
        filter_list = {'cm_code_type_id': self.request.data['cm_code_type_id']}

        # 파라미터를 쿼리셋에 적용
        queryset = CmCodeDetail.objects.filter(**filter_list)
        serializer = CmCodeDetailListSerializer(queryset, many=True)
        return_data = {"data": serializer.data}
        # Django가 아닌, DRF의 Response를 사용해야 함
        return Response(return_data)

    @swagger_auto_schema(method='post', request_body=CmTestListSerializer(), operation_description='기준코드 저장')
    @action(detail=False, methods=['post'])
    def save(self, request):
        LOGGER.debug('request - post')
        request_data = request.data
        # serializers = CmTestListSerializer
        # serialized = serializers(data=request_data, many=isinstance(request_data, list))
        # if serialized.is_valid():
        #     pass
        #     # serialized.save()
        # return Response(serialized.data)
        master_data = request_data['master']
        master_serializer = CmCodeMasterListSerializer(data=master_data, many=isinstance(master_data, list))

        return Response()


# 멀티 레코드를 업데이트하기 위한 테스트뷰 - 표준화는 추후 적용
# ViewSet을 사용하면, url과 ViewSet에 있는 메서드를 매핑할 수 있음.
# /api/basecode/master -> ViewSet.get_master, /api/basecode/detail -> ViewSet.get_detail
# @swagger_auto_schema 데코레이터를 사용하면 지정한 serializer를 이용하여 swagger ui에 스키마를 생성해 줌
# 다중 테이블을 이용해야하므로 각 메서드에서 queryset, serializers 생성하여 사용
class ProgramListViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, pk):
        # try:
        #     return ProgramModel.objects.get(pk=pk)
        # except (ProgramModel.DoesNotExists, ValidationError):
        #     raise status.HTTP_404_NOT_FOUND
        return ProgramModel.objects.get(pk=pk)

    @swagger_auto_schema(method='get', responses={200: ProgramSerializer(many=True), 404: '자료 없음'},
                         operation_description='프로그램 목록 조회')
    @action(detail=False, methods=['get'])
    def get(self, request):
        LOGGER.debug('request - get - get')
        # 조회 파라미터
        filter_list = {}
        # 조회 파라미터를 생성할 Dict 객체 생성 - request body에 조회 조건을 확인하여 적용
        if len(self.request.data) > 0:
            if 'system_code' in self.request.data and self.request.data['system_code'] != '%':
                filter_list['system_code'] = self.request.data['system_code']
            if 'pgm_type' in self.request.data and self.request.data['pgm_type'] != '%':
                filter_list['pgm_type'] = self.request.data['pgm_type']

        # 파라미터를 쿼리셋에 적용
        queryset = ProgramModel.objects.filter(**filter_list)
        LOGGER.debug(queryset.query)
        serializer = ProgramSerializer(queryset, many=True)

        # 조회시 반환할 데이터
        return_data = {'success': True, 'code': 1, 'message': 'OK', 'data': None}

        if len(serializer.data) == 0:
            msg = '조건에 맞는 자료가 없습니다.'
            LOGGER.error(msg)
            return_data['success'] = True
            return_data['code'] = 0
            return_data['message'] = msg
            return Response(return_data, status.HTTP_200_OK)

        # 조회한 데이터에 row 기본 상태값('unchanged')을 설정한다.
        for row in serializer.data:
            row['row_stat'] = 'unchanged'

        return_data['data'] = serializer.data

        # Django가 아닌, DRF의 Response를 사용해야 함
        return Response(return_data)

    @swagger_auto_schema(method='post', request_body=ProgramSerializer(many=True),
                         responses={200: ProgramSerializer(many=True)}, operation_description='프로그램 목록 저장')
    @action(detail=False, methods=['post'])
    def save(self, request):
        LOGGER.debug('request - post - save')

        # 반환할 데이터
        return_data = {'success': True, 'code': 1, 'message': 'OK', 'data': None}

        if len(request.data) == 0:
            return_data['success'] = False
            return_data['code'] = 0
            return_data['message'] = '저장할 데이터가 없습니다.'
            return Response(return_data, status.HTTP_400_BAD_REQUEST)

        request_data = request.data

        # serialized = ProgramSerializer(data=request_data, many=isinstance(request_data, list))
        # serialized.is_valid(raise_exception=False)
        # if not serialized.is_valid(raise_exception=False):
        #     return Response(serialized.data, status.HTTP_400_BAD_REQUEST)

        try:
            # Delete -> Update -> Insert
            with transaction.atomic():
                # Begin transaction
                self._perform_delete(request_data)
                self._perform_update(request_data)
                self._perform_insert(request_data)
                # End transaction
        except Exception as ex:
            return_data['success'] = False
            return_data['code'] = -1
            return_data['message'] = '예외 발생'
            # 예외 serialize 필요
            # return_data['data'] = ex
            return Response(return_data, status.HTTP_400_BAD_REQUEST)

        return Response(request_data, status.HTTP_200_OK)

    def _perform_insert(self, request_data):
        """신규 행을 Insert
        """
        # 저장할 칼럼 목록
        target_columns = ['pgm_id', 'pgm_name', 'system_code', 'pgm_type', 'pgm_url', 'use_yn', 'first_rg_yms',
                          'first_rg_idf', 'last_update_yms', 'last_update_idf']
        # Insert 대상 요청 데이터
        added_data = self._get_stat_rows(request_data, 'added')
        if len(added_data) > 0:
            # 저장할 칼럼만으로 구성된 행 추출
            target_rows = []
            for row in added_data:
                # 필요한 칼럼만 저장하기 위해 추출 -> 추후 보완 검토
                target_rows.append({key: value for key, value in row.items() if key in target_columns})

            # Serializer를 통해 저장, Model을 사용해도 됨
            serialized = ProgramSerializer(data=target_rows, many=isinstance(target_rows, list))
            if serialized.is_valid(raise_exception=False):
                serialized.save()

        # 저장 과정에서 변경된 데이터가 있을 수 있으므로.
        # 저장한 행의 정보를 요청 자료에 반영, row_stat는 added -> unchangd로 변경

    def _perform_update(self, request_data):
        """변경된 행 Update
        """
        # 저장할 칼럼 목록
        target_columns = ['pgm_id', 'pgm_name', 'system_code', 'pgm_type', 'pgm_url', 'use_yn', 'first_rg_yms',
                          'first_rg_idf', 'last_update_yms', 'last_update_idf']
        # Update 대상 요청 데이터
        modified_data = self._get_stat_rows(request_data, 'modified')
        if len(modified_data) > 0:
            # 저장할 칼럼만으로 구성된 행 추출
            target_rows = []
            for row in modified_data:
                # 필요한 칼럼만 저장하기 위해 추출 -> 추후 보완 검토
                target_rows.append({key: value for key, value in row.items() if key in target_columns})

            # 모델을 시용하여 저장, 요청 메서드가 POST여서 그런지 serializers.is_valid()에서 오류 발생함
            # PK가 여러개의 칼럼으로 구성된 경우 다른 방식 사용해야 함
            for row in target_rows:
                db_row = self.get_object(pk=row['pgm_id'])
                for key, value in row.items():
                    setattr(db_row, key, value)
                db_row.save()

    def _perform_delete(self, request_data):
        """삭제된 행 Delete
        """
        deleted_data = self._get_stat_rows(request_data, 'deleted')
        if len(deleted_data) > 0:
            for row in deleted_data:
                db_row = self.get_object(pk=row['pgm_id'])
                db_row.delete()

    def _get_stat_rows(self, data, row_stat):
        """지정한 상태의 행을 검색하여 리스트로 반환
        """
        result_data = list(filter(lambda x: x['row_stat'] == row_stat, data))
        return result_data


def TemplateDummyListView(request):
    print(request.META.get('Access-Control-Allow-Origin'))

    return JsonResponse({
        'success': True,
        'items': [{'id': 'tomas', 'name': 'tomas lee', 'sex': '1'},
                  {'id': 'foo', 'name': 'foo foo', 'sex': '2'},
                  {'id': 'bar', 'name': 'bar bar', 'sex': '1'}],
    }, json_dumps_params={'ensure_ascii': True})

# Specify downloads path
# path = os.path.dirname(os.path.abspath(__file__))

# @csrf_exempt
# def TemplateDummyFileView(request):
#     download_file = open(os.path.join(os.path.dirname(path), 'download/code/codes.json'), "rb")
#     response = HttpResponse(download_file, content_type='application/force-download')
#     response['Content-Disposition'] = 'attachment; filename="codes.json"'
#     return response


# TEST
class MetaInfoView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """request.META 확인용"""
        values = request.META
        meta_info = []
        for k in sorted(values):
            meta_info.append(f'''{k} - {request.META.get(k, 'n/a')}''')

        # Django가 아닌, DRF의 Response를 사용해야 함
        return_data = {"meta-info": meta_info}
        return Response(return_data)
