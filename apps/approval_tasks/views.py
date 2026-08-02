from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.approval_tasks.models import ApprovalTask
from apps.approval_tasks.serializers import ApprovalTaskSerializer

# Create your views here.


class ApprovalTaskView(GenericAPIView):
    serializer_class = ApprovalTaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = ApprovalTask.objects.all()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovalTaskDetailsView(GenericAPIView):
    serializer_class = ApprovalTaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(ApprovalTask, id=task_id)
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, task_id):
        task = get_object_or_404(ApprovalTask, id=task_id)
        serializer = self.get_serializer(task, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        task = get_object_or_404(ApprovalTask, id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
