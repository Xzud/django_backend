from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from apps.leave.models import Leave
from .serializers import LeaveSerializer

# Create your views here.

# POST /leave
# GET /leave
# GET /leave/{id}
# PATCH /leave/{id}/approve
# PATCH /leave/{id}/reject


class LeaveView(GenericAPIView):
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]
    queryset = Leave.objects.all()

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            leave = serializer.save()
            return Response(
                self.get_serializer(leave).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveWithIDView(GenericAPIView):
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, leave_id):
        leave = Leave.objects.get(id=leave_id)
        return Response(self.get_serializer(leave).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_approval_instance(request, leave_id):
    # Get Leave Object, Get Employee from user

    # Get workflow from request
    pass
