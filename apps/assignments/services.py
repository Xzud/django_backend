from .models import EmployeeShiftAssignment
from datetime import date
from django.db.models import Q


def get_all_employee_shift_assignment(employee_id):
    return EmployeeShiftAssignment.objects.filter(employee_id=employee_id)


def get_active_employee_shift_assignment(employee_id):
    return (
        EmployeeShiftAssignment.objects.filter(
            employee_id=employee_id, effective_from__lte=date.today()
        )
        .filter(Q(effective_to__gte=date.today()) | Q(effective_to__isnull=True))
        .order_by("-effective_from")
        .select_related("shift")
        .first()
    )
