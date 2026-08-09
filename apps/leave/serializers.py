from rest_framework.serializers import ModelSerializer

from apps.leave.models import Leave


class LeaveSerializer(ModelSerializer):
    class Meta:
        model = Leave
        exclude = ["created_at", "updated_at"]
