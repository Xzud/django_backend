from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.departments.models import Department
from apps.departments.serializers import DepartmentSerializer
from apps.employees.models import Employee
from apps.positions.models import EmployeePosition
from apps.positions.serializers import EmployeePositionSerializer
from apps.users.serializers import User, UserSerializer


class SupervisorSerializer(ModelSerializer):
    class Meta:
        model = Employee
        exclude = ["created_at", "updated_at"]
class EmployeeSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    position = EmployeePositionSerializer(read_only=True)
    supervisor = SupervisorSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    # Writable ID fields
    user_id = PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    position_id = PrimaryKeyRelatedField(
        source="position",
        queryset=EmployeePosition.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    supervisor_id = PrimaryKeyRelatedField(
        source="supervisor",
        queryset=Employee.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    department_id = PrimaryKeyRelatedField(
        source="department",
        queryset=Department.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Employee
        exclude = ["created_at", "updated_at"]
