from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ApprovalInstance
from .serializers import ApprovalInstanceSerializer

# Create your views here.


# TODO might need to change this as a utility focused instead of exposing to client since each request type approval instances will be handled by their own app
class ApprovalInstanceView(GenericAPIView):
    serializer_class = ApprovalInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO do prefetches with the minor important details [requester.name, request type, etc] for view purposes
        instances = ApprovalInstance.objects.all()
        serializer = ApprovalInstanceSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # TODO figure out how to do create with a polymorphic foreign key
        serializer = ApprovalInstanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(requester=request.user.employee_detail)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovalInstanceDetailView(GenericAPIView):
    serializer_class = ApprovalInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, approval_id):
        # TODO do prefetches with the related tables [workflow, current_steup, requester, request_obect(GenericPrefetch)] for view purposes
        instance = get_object_or_404(ApprovalInstance, id=approval_id)
        serializer = ApprovalInstanceSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, approval_id):
        instance = get_object_or_404(ApprovalInstance, id=approval_id)
        serializer = ApprovalInstanceSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, approval_id):
        instance = get_object_or_404(ApprovalInstance, id=approval_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
