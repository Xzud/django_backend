from rest_framework.serializers import ModelSerializer

from apps.employee_dayoffs.serializers import EmployeeDayOffSerializer
from apps.employees.serializers import EmployeeSerializer
from apps.shifts.serializers import EmployeeShiftSerializer
from .models import EmployeeShiftAssignment


class EmployeeShiftAssignmentSerializer(ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    shift = EmployeeShiftSerializer(read_only=True)
    assigned_by = EmployeeSerializer(read_only=True)
    days_off = EmployeeDayOffSerializer(many=True, read_only=True)

    class Meta:
        model = EmployeeShiftAssignment
        fields = [
            "employee",
            "shift",
            "effective_from",
            "effective_to",
            "assigned_by",
            "days_off",
        ]


class ESA_WriteSerializer(ModelSerializer):
    class Meta:
        model = EmployeeShiftAssignment
        fields = [
            "employee",
            "shift",
            "effective_from",
            "effective_to",
            "assigned_by",
        ]

    def to_representation(self, instance):
        return EmployeeShiftAssignmentSerializer(instance, context=self.context).data
