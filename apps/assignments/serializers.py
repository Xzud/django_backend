from rest_framework.serializers import ModelSerializer
from .models import EmployeeShiftAssignment


class EmployeeShiftAssignmentSerializer(ModelSerializer):
    class Meta:
        model = EmployeeShiftAssignment
        fields = [
            "employee",
            "shift",
            "effective_from",
            "effective_to",
            "assigned_by",
        ]
