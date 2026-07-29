from rest_framework.serializers import ModelSerializer
from .models import EmployeePosition


class EmployeePositionsSerializer(ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = [
            "name",
            "description",
            "level",
        ]
