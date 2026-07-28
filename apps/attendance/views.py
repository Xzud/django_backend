from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from apps.attendance.serializers import AttendanceSerializer
from apps.employees.models import Employee
from .models import Attendance

# Create your views here.

# POST /attendance/clock-in
# PATCH /attendance/clock-out/{attendance_id}
# GET /attendance
# GET /attendance/{employee_id}


class AttendanceClockInView(GenericAPIView):
    serializer_class = AttendanceSerializer

    # POST /attendance/clock-in OR consider /attendance/{employee_id}/clock_in
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            employee_id = serializer.data["employee"]
            employee = Employee.objects.get(id=employee_id)

            attendance = Attendance.objects.create(
                employee=employee,
                date=timezone.now().date(),
                clock_in=timezone.now(),
                status="Present",
            )
            attendance.save()

            return Response(
                self.get_serializer(attendance).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceClockOutView(GenericAPIView):
    serializer_class = AttendanceSerializer

    # PATCH /attendance/clock-out/{attendance_id}
    def patch(self, request, attendance_id):
        attendance = Attendance.objects.get(id=attendance_id)

        serializer = self.get_serializer(
            attendance, data={"clock_out": timezone.now()}, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceView(GenericAPIView):
    serializer_class = AttendanceSerializer

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

    @extend_schema(operation_id="single_attendance")
    def get(self, request, employee_id):
        try:
            attendance = Attendance.objects.get(employee=employee_id)
            serializer = self.get_serializer(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Attendance.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
