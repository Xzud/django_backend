from rest_framework.serializers import ModelSerializer
from .models import EmployeeDayOff


class EmployeeDayOffSerializer(ModelSerializer):
    class Meta:
        model = EmployeeDayOff
        fields = [
            "id",
            "assignment",
            "day_of_week",
        ]
