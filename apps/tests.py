from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from apps.employees.models import Employee
from apps.shifts.models import EmployeeShift, ShiftType


class CustomAPITestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            email="testuser@example.com",
            password="testuser123",
            role="employee",
        )

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

        self.client.force_authenticate(user=self.user)
