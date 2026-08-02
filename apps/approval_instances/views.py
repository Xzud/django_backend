from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ApprovalInstance
from .serializers import ApprovalInstanceSerializer

# Create your views here.


# TODO need to double check
class ApprovalInstanceView(GenericAPIView):
    serializer_class = ApprovalInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instances = ApprovalInstance.objects.all()
        serializer = ApprovalInstanceSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ApprovalInstanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovalInstanceDetailView(GenericAPIView):
    serializer_class = ApprovalInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, instance_id):
        instance = get_object_or_404(ApprovalInstance, id=instance_id)
        serializer = ApprovalInstanceSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, instance_id):
        instance = get_object_or_404(ApprovalInstance, id=instance_id)
        serializer = ApprovalInstanceSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, instance_id):
        instance = get_object_or_404(ApprovalInstance, id=instance_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
