from rest_framework import serializers

from core.serializers import BaseModelSerializer
from common.models.employee import CmEmployee, CmDepartment


class CmEmployeeSerializer(BaseModelSerializer):
    # 모델에 없는 칼럼 추가 - View에서 subquery로 채워넣는 칼럼
    dept_name = serializers.CharField(max_length=50, allow_blank=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = CmEmployee


class CmDepartmentSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CmDepartment
