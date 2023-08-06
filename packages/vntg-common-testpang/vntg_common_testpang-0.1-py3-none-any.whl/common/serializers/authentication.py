from rest_framework import serializers

from core.serializers import BaseModelSerializer
from common.models.authentication import CmGroupUsers, CmUserRole, CmGroupAuth, CmUserAuth


class CmUserGroupSerializer(BaseModelSerializer):
    # 모델에 없는 칼럼 추가 - View에서 subquery로 채워넣는 칼럼
    group_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    system_type = serializers.CharField(max_length=10, allow_blank=True, required=False)
    use_yn = serializers.CharField(max_length=1, allow_blank=True, required=False)
    remark = serializers.CharField(max_length=500, allow_blank=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = CmGroupUsers
        read_only_fields = ['group_name', 'system_type', 'use_yn', 'remark']


class CmGroupUsersSerializer(BaseModelSerializer):
    # 모델에 없는 칼럼 추가 - View에서 subquery로 채워넣는 칼럼
    user_name = serializers.CharField(max_length=100, allow_blank=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = CmGroupUsers
        read_only_fields = ['user_name']


class CmUserRoleSerializer(BaseModelSerializer):
    # 모델에 없는 칼럼 추가 - View에서 subquery로 채워넣는 칼럼
    role_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    role_type = serializers.CharField(max_length=100, allow_blank=True, required=False)
    system_yn = serializers.CharField(max_length=100, allow_blank=True, required=False)
    use_yn = serializers.CharField(max_length=100, allow_blank=True, required=False)
    remark = serializers.CharField(max_length=100, allow_blank=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = CmUserRole
        read_only_fields = ['role_name', 'system_yn']


class CmGroupAuthSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = CmGroupAuth
        read_only_fields = ['group_name']


class CmUserAuthSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = CmUserAuth
        read_only_field = ['user_name']
