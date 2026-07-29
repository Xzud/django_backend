from rest_framework.serializers import ModelSerializer
from .models import EmployeeDayOff


class EmployeeDayOffSerializer(ModelSerializer):
    class Meta:
        model = EmployeeDayOff
        fields = [
            "assignment",
            "day_of_week",
        ]
