from rest_framework import serializers

from apps.employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_number",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "hire_date",
            "status",
        ]
