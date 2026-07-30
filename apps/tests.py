from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from apps.assignments.models import EmployeeShiftAssignment
from apps.employees.models import Employee
from apps.positions.models import EmployeePosition
from apps.shifts.models import EmployeeShift, ShiftType


class CustomAPITestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            email="testuser@example.com",
            password="testuser123",
            role="employee",
        )

        self.client.force_authenticate(user=self.user)

        self.employee = Employee.objects.create(
            employee_number="EMP001",
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            hire_date="2024-01-01",
            status="active",
        )

        self.shifts = {
            "Morning Shift": EmployeeShift.objects.create(
                name="Morning Shift (First Shift)",
                shift_type=ShiftType.FIXED,
                start_time="08:00",
                end_time="17:00",
            ),
            "Graveyard Shift": EmployeeShift.objects.create(
                name="Graveyard Shift (Third Shift)",
                shift_type=ShiftType.FIXED,
                start_time="21:00",
                end_time="06:00",
            ),
        }

        manager_position = EmployeePosition.objects.create(name="Manager", level="100")
        ceo_position = EmployeePosition.objects.create(name="CEO", level="1000")

        self.manager = Employee.objects.create(
            employee_number="EMP002",
            first_name="Elton",
            last_name="John",
            email="elton.john@example.com",
            hire_date="2022-05-12",
            status="active",
            position=manager_position,
        )

        self.owner = Employee.objects.create(
            employee_number="EMP000",
            first_name="Kenny",
            last_name="Rogers",
            email="kenny.rogers@example.com",
            hire_date="2020-01-01",
            status="active",
            position=ceo_position,
        )

        self.first_employee_shift_assignment = EmployeeShiftAssignment.objects.create(
            employee=self.employee,
            shift=self.shifts["Morning Shift"],
            effective_from="2024-01-01",
            assigned_by=self.manager,
        )
