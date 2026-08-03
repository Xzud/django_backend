from rest_framework.serializers import ModelSerializer
from .models import ApprovalStep


class ApprovalStepSerializer(ModelSerializer):
    class Meta:
        model = ApprovalStep
        exclude = ["created_at", "updated_at"]
