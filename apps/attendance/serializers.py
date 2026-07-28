from rest_framework.serializers import ModelSerializer

from apps.attendance.models import Attendance


class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["employee", "date", "clock_in", "clock_out", "status"]
