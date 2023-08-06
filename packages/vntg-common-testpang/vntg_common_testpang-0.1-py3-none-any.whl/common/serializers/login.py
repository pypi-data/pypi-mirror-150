import logging

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.helper.log_helper import create_login_log
from common.views.user_group import UserDetailView
from core.helper import get_item_count
from core.helper.request_helper import get_current_request

LOGGER = logging.getLogger(__name__)


# JWT Payload 를 커스터마이징하기 위한 Serializer
class LoginSerializer(TokenObtainPairSerializer):
    """JWT Payload 를 커스터마이징하기 위한 Serializer"""

    @classmethod
    def get_token(cls, user):
        # 오버라이드
        token = super(LoginSerializer, cls).get_token(user)

        LOGGER.debug(f'Login - {user.user_name}')

        # Get User detail info
        user_info = UserDetailView()

        if user.system_type == 'S02':
            raise Exception('사용자 정보를 찾을 수 없습니다. (id 및 password를 확인해주세요.)')

        user_details = user_info.get_list_by_node_name(node_name='user-detail',
                                                       parameters={'p_user_id': user.user_id})
        user_detail = user_details[0]

        # Add Custom claims
        token['user_name'] = user.user_name
        token['corp_code'] = user_detail['corp_code']
        token['busi_place'] = user_detail['busi_place']
        token['busi_place_name'] = user_detail['busi_place_name']
        # token['dept_code'] = user_detail['dept_code']
        # token['dept_name'] = user_detail['dept_name']
        token['emp_no'] = user_detail['emp_no']
        token['emp_name'] = user_detail['emp_name']
        token['plant_code'] = user_detail['plant_code']
        token['plant_name'] = user_detail['plant_name']
        token['equip_code'] = user_detail['equip_code']
        token['equip_name'] = user_detail['equip_name']
        token['unit_work_code'] = user_detail['unit_work_code']
        token['unit_work_name'] = user_detail['unit_work_name']
        token['responsi'] = user_detail['responsi']
        token['responsi_name'] = user_detail['responsi_name']
        token['user_level'] = user_detail['user_level']
        token['system_type'] = user_detail['system_type']

        # 로그인 로그 생성
        create_login_log(user_id=user.user_id, request=get_current_request())

        return token

    def validate(self, attrs):
        # 오버라이드
        # data = super().validate(attrs)
        #
        # refresh = self.get_token(self.user)
        #
        # data['refresh'] = str(refresh)
        # data['access'] = str(refresh.access_token)
        #
        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)
        #
        # return data

        # data = super().validate(attrs)
        # refresh = self.get_token(self.user)

        data = super().validate(attrs=attrs)

        return_data = {
            'success': True,
            'code': 1,
            'message': 'OK',
            # 'data': {'refresh': str(refresh),
            #          'access': str(refresh.access_token)}
            'data': data
        }

        return return_data


class CustLoginSerializer(TokenObtainPairSerializer):
    """JWT Payload 를 커스터마이징하기 위한 Serializer"""

    @classmethod
    def get_token(cls, user):
        # 오버라이드
        token = super(CustLoginSerializer, cls).get_token(user)

        LOGGER.debug(f'Login - {user.user_name}')

        # Get User detail info
        user_info = UserDetailView()

        if user.system_type == 'S01':
            raise Exception('사용자 정보를 찾을 수 없습니다. (id 및 password를 확인해주세요.)')

        # 공사업체
        user_details = user_info.get_list_by_node_name(node_name='cust-user-detail',
                                                       parameters={'p_user_id': user.user_id})
        user_detail = user_details[0]

        # Add Custom claims
        token['user_name'] = user_detail['user_name']
        token['corp_code'] = user_detail['corp_code']
        token['busi_place'] = user_detail['busi_place']
        token['busi_place_name'] = user_detail['busi_place_name']
        token['emp_no'] = user_detail['emp_no']
        token['emp_name'] = user_detail['emp_name']
        token['plant_code'] = user_detail['plant_code']
        token['plant_name'] = user_detail['plant_name']
        token['equip_code'] = user_detail['equip_code']
        token['equip_name'] = user_detail['equip_name']
        token['unit_work_code'] = user_detail['unit_work_code']
        token['unit_work_name'] = user_detail['unit_work_name']
        token['responsi'] = user_detail['responsi']
        token['responsi_name'] = user_detail['responsi_name']
        token['user_level'] = user_detail['user_level']
        token['system_type'] = user_detail['system_type']

        token['cust_code'] = user_detail['cust_code']
        token['cust_name'] = user_detail['cust_name']
        token['biz_rg_no'] = user_detail['biz_rg_no']
        token['email'] = user_detail['email']
        token['tel_no'] = user_detail['tel_no']

        # 로그인 로그 생성
        create_login_log(user_id=user.user_id, request=get_current_request())

        return token

    def validate(self, attrs):
        data = super().validate(attrs=attrs)

        return_data = {
            'success': True,
            'code': 1,
            'message': 'OK',
            'data': data
        }

        return return_data
