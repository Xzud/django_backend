from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import ApprovalStep
from .serializers import ApprovalStepSerializer

# Create your views here.


class ApprovalStepView(GenericAPIView):
    serializer_class = ApprovalStepSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        steps = ApprovalStep.objects.all()
        serializer = ApprovalStepSerializer(steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ApprovalStepSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovalStepDetailView(GenericAPIView):
    serializer_class = ApprovalStepSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, step_id):
        step = get_object_or_404(ApprovalStep, id=step_id)
        serializer = ApprovalStepSerializer(step)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, step_id):
        step = get_object_or_404(ApprovalStep, id=step_id)
        serializer = ApprovalStepSerializer(step, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, step_id):
        step = get_object_or_404(ApprovalStep, id=step_id)
        step.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_workflow_steps(request, workflow_id):
    steps = ApprovalStep.objects.filter(workflow_id=workflow_id)
    serializer = ApprovalStepSerializer(steps, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
