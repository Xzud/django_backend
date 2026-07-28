from django.shortcuts import render
from django.utils import timezone
from rest_framework import status, views
from rest_framework.response import Response

from apps.attendance.serializers import AttendanceSerializer
from apps.employees.models import Employee
from .models import Attendance

# Create your views here.

# POST /attendance/clock-in
# PATCH /attendance/clock-out/{attendance_id}
# GET /attendance
# GET /attendance/{employee_id}


class AttendanceClockInOutView(views.APIView):

    # POST /attendance/clock-in OR consider /attendance/{employee_id}/clock_in
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)

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
                AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH /attendance/clock-out/{attendance_id}
    def patch(self, request, attendance_id):
        attendance = Attendance.objects.get(id=attendance_id)

        serializer = AttendanceSerializer(
            attendance, data={"clock_out": timezone.now()}, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceView(views.APIView):

    def get(self, request, employee_id=None):
        try:
            if employee_id:
                # TODO Check if employee = employee_id is correct
                attendance = Attendance.objects.get(employee=employee_id)
                serializer = AttendanceSerializer(attendance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                attendances = Attendance.objects.all()
                serializer = AttendanceSerializer(attendances, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
