from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.employees.models import Employee
from apps.positions.models import EmployeePosition
from apps.tests import CustomAPITestCase
from apps.shifts.models import EmployeeShift, ShiftType
from .models import EmployeeShiftAssignment

# Create your tests here.


class ESAssignmentTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

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

        self.first_shift = self.shifts["Morning Shift"]

        self.first_employee_shift_assignment = EmployeeShiftAssignment.objects.create(
            employee=self.employee,
            shift=self.first_shift,
            effective_from="2024-01-01",
            assigned_by=self.manager,
        )

    def test_fetch_all_assignments(self):
        url = reverse("assignment_list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["effective_from"],
            self.first_employee_shift_assignment.effective_from,
        )
        self.assertEqual(response.data[0]["shift"]["name"], self.first_shift.name)
        self.assertEqual(
            response.data[0]["shift"]["shift_type"], self.first_shift.shift_type
        )
        self.assertEqual(
            response.data[0]["employee"]["employee_number"],
            self.employee.employee_number,
        )
        self.assertEqual(
            response.data[0]["assigned_by"]["employee_number"],
            self.manager.employee_number,
        )

    def test_fetch_assignment_detail(self):
        url = reverse("assignment_detail", kwargs={"shift_assignment_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["effective_from"],
            self.first_employee_shift_assignment.effective_from,
        )
        self.assertEqual(response.data["shift"]["name"], self.first_shift.name)
        self.assertEqual(
            response.data["shift"]["shift_type"], self.first_shift.shift_type
        )
        self.assertEqual(
            response.data["employee"]["employee_number"],
            self.employee.employee_number,
        )
        self.assertEqual(
            response.data["assigned_by"]["employee_number"],
            self.manager.employee_number,
        )

    def test_create_assingment(self):
        url = reverse("create_assignment")
        test_assignment_details = {
            "employee": 2,
            "shift": 1,
            "effective_from": "2022-01-01",
            "assigned_by": 3,
        }

        response = self.client.post(url, test_assignment_details)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["effective_from"],
            test_assignment_details["effective_from"],
        )
        self.assertEqual(response.data["shift"]["name"], self.first_shift.name)
        self.assertEqual(
            response.data["shift"]["shift_type"], self.first_shift.shift_type
        )
        self.assertEqual(
            response.data["employee"]["employee_number"],
            self.manager.employee_number,
        )
        self.assertEqual(
            response.data["assigned_by"]["employee_number"],
            self.owner.employee_number,
        )

    def test_edit_assignment(self):
        url = reverse("edit_assignment", kwargs={"shift_assignment_id": 1})

        second_shift = EmployeeShift.objects.create(
            name="Evening Shift (Second Shift)",
            shift_type=ShiftType.FIXED,
            start_time="13:00",
            end_time="22:00",
        )

        new_shift_assignment = {
            "shift": second_shift.id,
            "effective_from": "2026-01-01",
        }

        response = self.client.patch(url, new_shift_assignment)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["shift"]["name"], second_shift.name)
        self.assertEqual(
            response.data["effective_from"], new_shift_assignment["effective_from"]
        )

    def test_delete_assignment(self):
        url = reverse("assignment_detail", kwargs={"shift_assignment_id": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
