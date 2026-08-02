from rest_framework.serializers import ModelSerializer
from apps.approval_instances.models import ApprovalInstance


class ApprovalInstanceSerializer(ModelSerializer):
    class Meta:
        model = ApprovalInstance
        fields = "__all__"
        exclude = ["created_at", "updated_at"]
