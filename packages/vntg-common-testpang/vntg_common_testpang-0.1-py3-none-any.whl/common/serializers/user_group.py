from core.serializers import BaseModelSerializer
from common.models.user_group import CmUser, CmGroup, CmRole


class CmUserSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmUser
        # 비밀번호 칼럼 제외
        fields = ('user_id', 'user_name', 'system_type', 'user_level', 'use_yn', 'emp_no', 'tel_no', 'email',
                  'remark', 'first_rg_yms', 'first_rg_idf', 'last_update_yms', 'last_update_idf')


class CmGroupSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmGroup


class CmRoleSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmRole
