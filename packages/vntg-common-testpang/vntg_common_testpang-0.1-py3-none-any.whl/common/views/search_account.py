import logging
import base64
import random
import string

from django.contrib.auth.hashers import make_password
from django.utils.datetime_safe import datetime
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

import core.constants
from apps.mail.mail_helper import send_mail
from core.business import BusinessNode
from core.helper.db_helper import execute_dml
from core.helper.file_helper import SqlFileHelper
from core.views.baseview import  BaseSqlApiView

from common.models.user_group import CmUser
LOGGER = logging.getLogger(__name__)


# 코드 페이지, 기본 값은 949(ks_c_5601-1987)
code_page = 949
encoding = 'ks_c_5601-1987'


def string_to_base64(value: str) -> str:
    """문자열을 Base64 인코딩하여 반환합니다."""

    # 문자열을 bytes 타입으로 인코딩 변환
    str_bytes = value.encode(encoding)
    # bytes 타입을 base64로 다시 변환
    base64_result = base64.b64encode(str_bytes)
    # base64 타입의 bytest 타입을 디코딩
    base64_str = base64_result.decode(encoding)

    return base64_str


def base64_decoding(value: str) -> str:
    """Base64 디코딩하여 반환합니다."""

    base64_str = value
    str_bytes = base64.b64decode(base64_str)
    init_str = str_bytes.decode('utf-8')
    return init_str


def make_random_string(string_length: int = 8):
    """지정한 자릿수의 랜덤한 문자열을 생성합니다. 예: 비밀번호

    :param string_length: 문자열 자릿수
    :return: 지정한 자릿수의 랜던 문자열
    """
    # 비밀번호 대상 문자
    pw_candidate = string.ascii_letters + string.digits + '~!@$*'

    random_string = ''
    for i in range(string_length):
        random_string += random.choice(pw_candidate)

    return random_string


# 아이디 찾기
class FindIdView(BaseSqlApiView):
    """사용자 목록의 ID 검색
    """

    permission_classes = (permissions.AllowAny,)

    # region 노드 정의

    def define_nodes(self):
        """비즈니스 로직 실행(조회/저장)에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # Id 찾기
        node_list_id = BusinessNode()
        node_list_id.node_name = 'find-id'
        node_list_id.sql_filename = 'find_id'
        node_list_id.table_name = 'cm_user'
        node_list_id.model = CmUser
        self._append_node(node_list_id)

    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):

        # 파라미터 설정
        filter_data = {
            'p_user_name': request_data.get('p_user_name'),
            'p_email': request_data.get('p_email'),
            'p_system_type': request_data.get('p_system_type'),
        }

        return filter_data

    @action(detail=False, methods=['post'])
    def get_find_id(self, request, *args, **kwargs):

        # request path를 이용하여 노드 검색
        node_name = 'find-id'

        # 조회
        serialized_data = self.get_list_by_node_name(node_name=node_name, parameters=request.data)

        if len(serialized_data) == 0:
            return Response({'success': True, 'code': 0, 'message': '해당하는 ID가 존재하지 않습니다.', 'data': False},
                            status.HTTP_200_OK)
        else:
            # 계정 정보
            user_id = list(item['user_id'] for item in serialized_data)

            return Response({'success': True, 'code': 1, 'message': f' ID 찾기에 성공했습니다.',
                             'data':  '아이디는 ' + str(", ".join(user_id)) + ' 입니다.'},
                            status.HTTP_200_OK)

    # endregion


# 비밀번호 찾기
class FindPasswordView(BaseSqlApiView):
    """사용자 목록의 ID 검색
    """

    permission_classes = (permissions.AllowAny,)

    # region 노드 정의

    def define_nodes(self):
        """비즈니스 로직 실행(조회/저장)에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # Pw 찾기
        node_list_pw = BusinessNode()
        node_list_pw.node_name = 'find-pw'
        node_list_pw.sql_filename = 'find_pw'
        node_list_pw.table_name = 'cm_user'
        node_list_pw.model = CmUser
        self._append_node(node_list_pw)

    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):

        # 파라미터 설정
        filter_data = {
            'p_user_id': request_data.get('p_user_id'),
            'p_email': request_data.get('p_email'),
            'p_system_type': request_data.get('p_system_type'),
        }

        return filter_data

    @action(detail=False, methods=['post'])
    def get_find_pw(self, request, *args, **kwargs):

        # request path 를 이용하여 노드 검색
        node_name = 'find-pw'

        # 조회
        serialized_data = self.get_list_by_node_name(node_name=node_name, parameters=request.data)

        # 접속 URL
        url = request.data.get('url')

        if len(serialized_data) == 0:
            return Response({'success': True, 'code': 0, 'message': '해당 ID의 정보가 없습니다. 관리자에게 문의 바랍니다.', 'data': False},
                            status.HTTP_200_OK)
        elif len(serialized_data) > 1:
            return Response({'success': True, 'code': 0, 'message': '해당 ID의 정보가 2건 이상입니다. 관리자에게 문의 바랍니다.',
                             'data': False},
                            status.HTTP_200_OK)
        else:
            # 계정 정보
            user_id = serialized_data[0].get('user_id')
            user_name = serialized_data[0].get('user_name')
            user_email = serialized_data[0].get('email')
            user_system_type = serialized_data[0].get('system_type')

            if user_system_type == 'S01':
                url_type = 'init-pw'
            else:
                url_type = 'cust-init-pw'

            account_encoding = string_to_base64(user_id + '|' + user_email + '|' + user_system_type)
            # 아이디 정보 메일 전송
            mail_type = 'EM20'
            sender = '세아제강 SHE <seahst_she@seah.co.kr>'
            recipient = [user_email]
            subject = '[SHE] 비밀번호 찾기 정보 안내'
            body = f''' 계정 정보 안내 메일입니다.\r\n
비밀번호 초기화 링크를 클릭해주세요.\r\n
\r\n
* 아이디: {user_id}\r\n
* 성명: {user_name}\r\n
* 비밀번호 초기화 링크: {url}/{url_type}/{account_encoding}\r\n
\r\n
'''
            result = send_mail(sender=sender,
                               recipient=recipient,
                               subject=subject,
                               body=body,
                               is_html=False,
                               mail_type=mail_type)

            return Response({'success': True, 'code': 1, 'message': f' {user_email}  주소로 초기화 메일을 전송했습니다.',
                             'data': True},
                            status.HTTP_200_OK)

    # endregion


# 비밀번호 초기화
class ResetPasswordView(BaseSqlApiView):
    """사용자 목록의 ID 검색
    """

    permission_classes = (permissions.AllowAny,)

    # region 노드 정의

    def define_nodes(self):
        """비즈니스 로직 실행(조회/저장)에 필요한 노드 정의"""
        # SqlFileHelper 등록
        self._sql_helper = SqlFileHelper(__package__)

        # Pw 초기화
        node_list_reset_pw = BusinessNode()
        node_list_reset_pw.node_name = 'init-pw'
        node_list_reset_pw.model = CmUser
        node_list_reset_pw.sql_filename = 'find_pw'
        node_list_reset_pw.table_name = 'cm_user'
        self._append_node(node_list_reset_pw)

    # endregion

    # region 조회

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):

        # 파라미터 설정

        account_decoding = base64_decoding(request_data.get('p_user_info'))
        user_id = account_decoding.split('|')[0]
        user_mail = account_decoding.split('|')[1]
        user_system_type = account_decoding.split('|')[2]

        filter_data = {
            'p_user_id': user_id,
            'p_email': user_mail,
            'p_system_type': user_system_type,
        }

        return filter_data

    @action(detail=False, methods=['post'])
    def reset_pw(self, request, *args, **kwargs):

        # request path 를 이용하여 노드 검색
        node_name = 'init-pw'

        # 조회
        serialized_data = self.get_list_by_node_name(node_name=node_name, parameters=request.data)

        if len(serialized_data) == 0:
            return Response({'success': True, 'code': 0, 'message': '해당 ID의 정보가 없습니다. 관리자에게 문의 바랍니다.', 'data': False},
                            status.HTTP_200_OK)
        elif len(serialized_data) > 1:
            return Response(
                {'success': True, 'code': 0, 'message': '해당 ID의 정보가 2건 이상입니다. 관리자에게 문의 바랍니다.', 'data': False},
                status.HTTP_200_OK)
        else:
            # 계정 정보
            user_id = serialized_data[0].get('user_id')
            user_email = serialized_data[0].get('email')
            user_system_type = serialized_data[0].get('system_type')
            password = make_random_string()
            hashed_password = make_password(password)
            parameters = {
                'p_user_id': user_id,
                'p_email': user_email,
                'p_pwd': hashed_password,
                'p_last_update_yms': datetime.now(),
                'p_system_type': user_system_type
            }

            # 임시 테이블 데이터를 본 테이블에 등록 (select/insert query 실행)
            affected_bool = execute_dml(cmd=self._sql_helper.get_query('init_pw'), parameters=parameters)

            if affected_bool:
                return Response(
                    {'success': True, 'code': 0, 'message': '초기화 성공', 'data': password},
                    status.HTTP_200_OK)

    # endregion
