from rest_framework.serializers import ModelSerializer

from apps.departments.serializers import DepartmentSerializer
from apps.employees.models import Employee
from apps.positions.serializers import EmployeePositionSerializer
from apps.users.serializers import UserSerializer


class EmployeeSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    position = EmployeePositionSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Employee
        exclude = ["created_at", "updated_at"]
