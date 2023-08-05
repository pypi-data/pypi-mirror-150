from core.serializers import BaseModelSerializer
from common.models.program_menu import CmProgram, CmMenu, CmMenuPgm, CmMenuParam, CmMenuTree


class CmProgramSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmProgram


class CmMenuSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmMenu


class CmMenuPgmSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmMenuPgm


class CmMenuParamSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmMenuParam


class CmMenuTreeSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmMenuTree
