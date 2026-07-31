from rest_framework.serializers import ModelSerializer

from apps.leave.models import Leave


class LeaveSerializer(ModelSerializer):
    class Meta:
        model = Leave
        fields = [
            "id",
            "employee",
            "type",
            "start_date",
            "end_date",
            "reason",
            # TODO figure how to make some fields readable only
            "status",
            "approved_by",
        ]
