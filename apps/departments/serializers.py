from rest_framework.serializers import ModelSerializer

from apps.departments.models import Department


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields=[
            "name",
            "description",
            "manager"
        ]