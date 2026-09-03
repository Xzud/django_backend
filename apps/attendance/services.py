from django.utils import timezone

from apps.employees.models import Employee
from apps.employees.services import fetch_employee
from apps.assignments.services import get_active_employee_shift_assignment
from apps.shifts.models import EmployeeShift
from .errors import EmployeeNotFoundError, NotAnEmployeeError

from .models import Attendance

def attendance_clockin(user_id, employee: Employee = None):
    if not employee:
        employee = fetch_employee(user_id=user_id)

    if employee is None:
        raise EmployeeNotFoundError(
            f"No employee found for user_id={user_id}"
        )

    if not isinstance(employee, Employee):
        raise NotAnEmployeeError(
            f"Expected Employee, got {type(employee).__name__} instead."
        )
    
    clock_in = timezone.localtime()

    attendance = get_latest_attendance(employee.id)
    if not attendance.clock_out:
        return attendance

    shift = get_active_employee_shift_assignment(employee.id).shift
    status = Attendance.Status.PRESENT

    if shift.shift_type == EmployeeShift.ShiftType.FIXED:
        if shift.start_time > shift.end_time:
            if clock_in.time() > shift.start_time or clock_in.time() < shift.end_time:
                status = Attendance.Status.LATE
        else:
            if clock_in.time() > shift.start_time and clock_in.time() < shift.end_time:
                status = Attendance.Status.LATE

    attendance = Attendance.objects.create(
        employee=employee,
        date=timezone.now().date(),
        clock_in=clock_in,
        status=status,
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
