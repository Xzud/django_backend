from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from apps.approval_workflows.models import ApprovalWorkflow
from apps.approval_workflows.serializers import ApprovalWorkflowSerializer

# Create your views here.


class ApprovalWorkflowView(GenericAPIView):
    serializer_class = ApprovalWorkflowSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workflows = ApprovalWorkflow.objects.all()
        serializer = self.serializer_class(workflows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                created_by=request.user.employee_detail
            )  # TODO check if this is acutally correct
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovalWorkflowDetailView(GenericAPIView):
    serializer_class = ApprovalWorkflowSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, workflow_id):
        workflow = get_object_or_404(ApprovalWorkflow, id=workflow_id)
        serializer = ApprovalWorkflowSerializer(workflow)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, workflow_id):
        workflow = get_object_or_404(ApprovalWorkflow, id=workflow_id)
        serializer = ApprovalWorkflowSerializer(
            workflow, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, workflow_id):
        workflow = get_object_or_404(ApprovalWorkflow, id=workflow_id)
        workflow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
