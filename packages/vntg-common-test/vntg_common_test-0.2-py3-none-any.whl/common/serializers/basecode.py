from core.serializers import BaseModelSerializer
from common.models.basecode import CmCodeMaster, CmCodeDetail


class CmCodeDetailSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmCodeDetail


class CmCodeMasterSerializer(BaseModelSerializer):
    code_detail = CmCodeDetailSerializer(many=True, read_only=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = CmCodeMaster
