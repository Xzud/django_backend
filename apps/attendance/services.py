from django.utils import timezone

from apps.employees.models import Employee
from apps.employees.services import fetch_employee

from .models import Attendance


def attendance_clockin(user_id, employee=None):
    if not employee:
        employee = fetch_employee(user_id=user_id)

    attendance = get_latest_attendance(employee.id)
    if not attendance.clock_out:
        return attendance

    # TODO check schedule first before creating attendance
    attendance = Attendance.objects.create(
        employee=employee,
        date=timezone.now().date(),
        clock_in=timezone.now(),
        status="Present",
    )
    attendance.save()

    return attendance


def attendance_clock_out(user_id, employee=None):
    if not employee:
        employee = fetch_employee(user_id=user_id)

    attendance = get_latest_attendance(employee.id)
    if attendance.clock_out:
        return attendance


# ================ Helpers ===================


def get_latest_attendance(employee_id):
    return (
        Attendance.objects.filter(employee_id=employee_id).order_by("-clock_in").first()
    )


def get_all_employee_attendance(employee_id):
    return Attendance.objects.order_by("-clock_in").filter(employee=employee_id)
