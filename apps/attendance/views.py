from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from apps.attendance.serializers import AttendanceSerializer
from apps.attendance.services import attendance_clockin
from apps.employees.models import Employee
from .models import Attendance

# Create your views here.

# POST /attendance/clock-in
# PATCH /attendance/clock-out/{attendance_id}
# GET /attendance
# GET /attendance/{employee_id}


class AttendanceClockInView(GenericAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    # POST /attendance/clock-in
    def post(self, request):
        attendance = attendance_clockin(request.user.id)
        return Response(
            self.get_serializer(attendance).data, status=status.HTTP_201_CREATED
        )


class AttendanceClockOutView(GenericAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    # PATCH /attendance/clock-out/{attendance_id}
    def patch(self, request, attendance_id):
        attendance = Attendance.objects.get(id=attendance_id)

        serializer = self.get_serializer(
            attendance, data={"clock_out": timezone.now()}, partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceView(GenericAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(operation_id="all_attendance")
    def get(self, request):
        try:
            attendances = Attendance.objects.all()
            serializer = self.get_serializer(attendances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceViewID(GenericAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(operation_id="single_attendance")
    def get(self, request, employee_id):
        try:
            attendance = Attendance.objects.order_by("-clock_in").filter(employee=employee_id)
            serializer = self.get_serializer(attendance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Attendance.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
