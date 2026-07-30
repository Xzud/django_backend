from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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


class ApproveLeaveView(GenericAPIView):
    # TODO create a logic that only allow superior to approve leave
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, leave_id):
        leave = Leave.objects.get(id=leave_id)
        serializer = self.get_serializer(
            leave,
            data={"status": "approved", "approved_by": request.user.id},
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RejectLeaveView(GenericAPIView):
    # TODO create a logic that only allow superior to reject leave
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, leave_id):
        leave = Leave.objects.get(id=leave_id)
        serializer = self.get_serializer(
            leave,
            data={"status": "rejected", "approved_by": request.user.id},
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
