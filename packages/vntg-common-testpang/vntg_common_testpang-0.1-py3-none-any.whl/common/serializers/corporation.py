from rest_framework import serializers

from core.serializers import BaseModelSerializer
from common.models.corporation import CmCorporation, CmBusiplace


class CmBusiplaceSerializer(BaseModelSerializer):
    # 모델에 없는 칼럼 추가 - View에서 subquery로 채워넣는 칼럼
    corp_name = serializers.CharField(max_length=50, allow_blank=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = CmBusiplace


class CmCorporationSerializer(BaseModelSerializer):
    # busi_place = CmBusiplaceSerializer(many=True, read_only=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = CmCorporation
