from datetime import date
from django.core.management.base import BaseCommand

from django.db import transaction
from apps.shifts.models import EmployeeShift
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

from apps.assignments.models import EmployeeShiftAssignment


class Command(BaseCommand):
    help = "Seed employees with positions"

    def handle(self, *args, **options):
        employees = Employee.objects.prefetch_related("shift_assignments").all()
        shifts = EmployeeShift.objects.all()

        for i, employee in enumerate(employees):
            if not employee.shift_assignments.exists():
                EmployeeShiftAssignment.objects.create(
                    employee=employee,
                    shift=shifts[i % 3],
                    effective_from=date.today()
                )
