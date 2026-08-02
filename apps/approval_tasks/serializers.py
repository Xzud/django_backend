from rest_framework.serializers import ModelSerializer
from .models import ApprovalTask


class ApprovalTaskSerializer(ModelSerializer):
    class Meta:
        model = ApprovalTask
        fields = "__all__"
        exclude = ["created_at", "updated_at"]
