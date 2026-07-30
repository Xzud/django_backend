from rest_framework.serializers import ModelSerializer
from .models import EmployeeShift


class EmployeeShiftSerializer(ModelSerializer):
    class Meta:
        model = EmployeeShift
        fields = [
            "name",
            "shift_type",
            "start_time",
            "end_time",
            "required_hours_per_day",
            "required_hours_per_week",
            "break_minutes",
            "grace_period_minute",
        ]
