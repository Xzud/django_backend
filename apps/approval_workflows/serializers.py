from rest_framework.serializers import ModelSerializer

from apps.approval_workflows.models import ApprovalWorkflow


class ApprovalWorkflowSerializer(ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = "__all__"
