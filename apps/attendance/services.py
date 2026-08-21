from django.utils import timezone

from apps.employees.models import Employee
from apps.employees.services import fetch_employee

from .models import Attendance


def attendance_clockin(user_id, employee=None):
    if not employee:
        employee = fetch_employee(user_id=user_id)

    attendance = Attendance.objects.create(
        employee=employee,
        date=timezone.now().date(),
        clock_in=timezone.now(),
        status="Present",
    )
    attendance.save()

    return attendance


def attendance_clock_out(user_id, attendance=None):
    pass