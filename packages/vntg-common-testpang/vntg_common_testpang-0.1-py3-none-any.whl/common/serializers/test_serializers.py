"""코드 참고 용
"""
from rest_framework import serializers
from common.models.basecode import CmCodeMaster, CmCodeDetail
from common.models.test_models import ProgramModel


class BaseReturnSerializer:
    def __init__(self, **kwargs):
        self.success = ''
        self.code = 0
        self.message = ''
        self.data = None

    def set_result(self, success, code, message):
        self.success = success
        self.code = code
        self.message = message

    def set_result(self, success, code, message, data):
        self.success = success
        self.code = code
        self.message = message
        self.data = data


# 기본 모델
class BaseModelSerializer(serializers.ModelSerializer):
    # 모델에 없는 칼럼 추가
    # row_stat = serializers.CharField(max_length=20, allow_null=True, allow_blank=True, required=False, default='unchanged')
    pass


class CmCodeDetailListSerializer(BaseModelSerializer):
    class Meta:
        model = CmCodeDetail
        fields = '__all__'


class CmCodeMasterListSerializer(BaseModelSerializer):
    # Nested serializers
    # child = CmCodeDetailListSerializer()

    class Meta:
        model = CmCodeMaster
        fields = '__all__'


class CmTestListSerializer(serializers.Serializer):
    master = CmCodeMasterListSerializer(many=True)
    detail = CmCodeDetailListSerializer(many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = '__all__'


# class ProgramListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass
#
#     def delete(self, instance):
#         pass


class ProgramSerializer(BaseModelSerializer):
    class Meta:
        model = ProgramModel
        fields = '__all__'
        # list_serializer_class = ProgramListSerializer

    # def save(self, **kwargs):
    #     self.fields = {'pgm_id', 'pgm_name', 'system_code', 'pgm_type', 'pgm_url', 'use_yn', 'first_rg_yms', 'first_rg_idf', 'last_update_yms', 'last_update_idf'}
    #     super().save(**kwargs)
