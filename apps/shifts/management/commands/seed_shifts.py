from datetime import time

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.employees.models import Employee

from apps.positions.models import EmployeePosition
from apps.shifts.models import EmployeeShift
from apps.shifts.serializers import EmployeeShiftSerializer


class Command(BaseCommand):
    help = "Seed employees with positions"

    def handle(self, *args, **options):
        employees = Employee.objects.all()

        shifts = [
            {
                "name": "Fixed Schedule",
                "shift_type": EmployeeShift.ShiftType.FIXED,
                "start_time": time(8, 0),
                "end_time": time(17, 0),
            },
            {
                "name": "Flexible Daily Hours Schedule",
                "shift_type": EmployeeShift.ShiftType.FLEX_DAILY,
                "required_hours_per_day": 8,
            },
            {
                "name": "Flexible Weekly Hours Schedule",
                "shift_type": EmployeeShift.ShiftType.FLEX_WEEKLY,
                "required_hours_per_week": 40,
            },
        ]

        for shift in shifts:
            try:
                with transaction.atomic():
                    serializer = EmployeeShiftSerializer(data=shift)
                    if serializer.is_valid():
                        serializer.save()
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Seeding {shift.name} failed. Already exist. \n{e}"
                    )
                )

        # print(f"positions: {positions}")

        # for i, employee in enumerate(employees):
        #     if not employee.position:
        #         position, _ = positions[i % 3]["object"]
        #         employee.position = position
        #         employee.save()
