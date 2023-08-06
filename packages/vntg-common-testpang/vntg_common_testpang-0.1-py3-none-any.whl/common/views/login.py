import logging

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from common.serializers.login import LoginSerializer, CustLoginSerializer
from core.helper.request_helper import get_current_user

LOGGER = logging.getLogger(__name__)


# JWT Payload 를 커스터마이징하기 위한 View
class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.system_type = 'S01'

        try:
            serializer.is_valid(raise_exception=True)
        # except TokenError as e:
        #     raise InvalidToken(e.args[0])
        except Exception as ex:
            # 로그인 실패하면 커스텀 메시지 반환.
            return_data = {'success': False,
                           'code': 0,
                           'message': '사용자 정보를 찾을 수 없습니다. (id 및 password를 확인해주세요.)',
                           'data': str(ex)
                           }
            return Response(return_data, status.HTTP_200_OK)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# JWT Payload 를 커스터마이징하기 위한 View
class CustLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.system_type = 'S01'

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as ex:
            # 로그인 실패하면 커스텀 메시지 반환.
            return_data = {'success': False,
                           'code': 0,
                           'message': '사용자 정보를 찾을 수 없습니다. (id 및 password를 확인해주세요.)',
                           'data': str(ex)
                           }
            return Response(return_data, status.HTTP_200_OK)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
