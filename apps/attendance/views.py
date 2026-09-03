from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .errors import EmployeeNotFoundError,NotAnEmployeeError

from drf_spectacular.utils import extend_schema


from apps.attendance.serializers import AttendanceSerializer
from apps.attendance.services import (
    attendance_clockin,
    get_all_employee_attendance,
    get_latest_attendance,
)
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
        try:
            attendance = attendance_clockin(request.user.id)
            return Response(
                self.get_serializer(attendance).data, status=status.HTTP_201_CREATED
            )
        
        except (EmployeeNotFoundError, NotAnEmployeeError) as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AttendanceClockOutView(GenericAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    # POST /attendance/clock-out/
    def post(self, request):

        employee = request.user.employee_detail
        attendance = get_latest_attendance(employee.id)

        if attendance.clock_out:
            return Response(
                {"message": "Already clocked-out."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(
            attendance, data={"clock_out": timezone.now()}, partial=True
        )

        if serializer.is_valid():
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
            attendance = get_all_employee_attendance(employee_id)
            serializer = self.get_serializer(attendance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Attendance.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    attendance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
