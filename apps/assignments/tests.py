from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.assignments.models import EmployeeShiftAssignment
from apps.tests import CustomAPITestCase
from apps.shifts.models import EmployeeShift, ShiftType

# Create your tests here.


class ESAssignmentTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        self.new_shift_assignment = EmployeeShiftAssignment.objects.create(
            employee=self.employee,
            shift=self.shifts["Graveyard Shift"],
            effective_from="2026-06-01",
            assigned_by=self.manager,
        )

        self.new_manager_shift_assignment = EmployeeShiftAssignment.objects.create(
            employee=self.manager,
            shift=self.shifts["Graveyard Shift"],
            effective_from="2026-04-01",
            assigned_by=self.owner,
        )

    def test_fetch_all_assignments(self):
        url = reverse("assignment_list")

        response = self.client.get(url)
        total_assignments = EmployeeShiftAssignment.objects.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), total_assignments)
        self.assertEqual(
            response.data[0]["effective_from"],
            self.first_employee_shift_assignment.effective_from,
        )
        self.assertEqual(
            response.data[0]["shift"]["name"], self.shifts["Morning Shift"].name
        )
        self.assertEqual(
            response.data[0]["shift"]["shift_type"],
            self.shifts["Morning Shift"].shift_type,
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
        self.assertEqual(
            response.data["shift"]["name"], self.shifts["Morning Shift"].name
        )
        self.assertEqual(
            response.data["shift"]["shift_type"],
            self.shifts["Morning Shift"].shift_type,
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
        self.assertEqual(
            response.data["shift"]["name"], self.shifts["Morning Shift"].name
        )
        self.assertEqual(
            response.data["shift"]["shift_type"],
            self.shifts["Morning Shift"].shift_type,
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

    def test_employee_assignment_shift(self):
        url = reverse("employe_shift", kwargs={"employee_id": 1})
        response = self.client.get(url)

        total_assignments = EmployeeShiftAssignment.objects.filter(
            employee_id=1
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(total_assignments, 0)

        for item in response.data:
            self.assertEqual(item["employee"]["id"], self.employee.id)

    def test_employee_active_assignment_shift(self):
        url = reverse("active_employe_shift", kwargs={"employee_id": 1})

        # Creating a future date
        future_shift = EmployeeShiftAssignment.objects.create(
            employee=self.employee,
            shift=self.shifts["Morning Shift"],
            effective_from=timezone.localdate() + timedelta(days=30),
            assigned_by=self.manager,
        )

        active_shift = EmployeeShiftAssignment.objects.create(
            employee=self.employee,
            shift=self.shifts["Morning Shift"],
            effective_from=timezone.localdate() - timedelta(days=30),
            assigned_by=self.manager,
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assertion to exclude future shift assignments
        self.assertNotEqual(response.data["id"], future_shift.id)
        self.assertNotEqual(
            response.data["effective_from"], future_shift.effective_from
        )

        # active_shift is valid
        self.assertEqual(response.data["id"], active_shift.id)
        self.assertEqual(response.data["shift"]["name"], active_shift.shift.name)
        self.assertEqual(
            response.data["effective_from"], active_shift.effective_from.isoformat()
        )
        self.assertEqual(response.data["effective_to"], None)

        active_shift.effective_to = timezone.localdate() - timedelta(days=20)
        active_shift.save()

        # active_shift is expired, must fallback to graveyard shift from setUp
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.new_shift_assignment.id)
        self.assertEqual(
            response.data["shift"]["name"], self.new_shift_assignment.shift.name
        )
        self.assertEqual(
            response.data["effective_from"], self.new_shift_assignment.effective_from
        )
