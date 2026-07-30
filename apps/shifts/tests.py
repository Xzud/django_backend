from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.shifts.models import ShiftType
from apps.tests import CustomAPITestCase

# Create your tests here.


class EmployeeShiftTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

    def test_get_all_employee_shifts(self):
        url = reverse("employee_shifts")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee_shift(self):
        url = reverse("employee_shifts")
        second_shift = {
            "name": "Evening Shift (Second Shift)",
            "shift_type": ShiftType.FIXED,
            "start_time": "13:00:00",
            "end_time": "22:00:00",
        }

        response = self.client.post(url, second_shift)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], second_shift["name"])
        self.assertEqual(response.data["shift_type"], second_shift["shift_type"])
        self.assertEqual(response.data["start_time"], second_shift["start_time"])
        self.assertEqual(response.data["end_time"], second_shift["end_time"])

    def test_delete_employee_shift(self):
        url = reverse("delete_employee_shift", kwargs={"shift_id": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
