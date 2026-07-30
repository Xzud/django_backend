from django.urls import reverse

from rest_framework import status

from apps.tests import CustomAPITestCase
from .models import EmployeeDayOff, DayOfWeek

# Create your tests here.


class EmployeeDayOffTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        saturday_off = EmployeeDayOff.objects.create(
            assignment=self.first_employee_shift_assignment,
            day_of_week=DayOfWeek.SATURDAY,
        )

    def test_get_shift_dayoffs(self):
        url = reverse("employee_dayoffs")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_dayoff(self):
        url = reverse("employee_dayoffs")
        dayoff_details = {
            "assignment": self.first_employee_shift_assignment.id,
            "day_of_week": DayOfWeek.SUNDAY,
        }
        response = self.client.post(url, dayoff_details)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["assignment"], dayoff_details["assignment"])
        self.assertEqual(response.data["day_of_week"], dayoff_details["day_of_week"])

    def test_delete_dayoffs(self):
        url = reverse("delete_employee_dayoff", kwargs={"dayoff_id": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_assignment_dayoffs(self):
        url = reverse(
            "assignment_dayoffs",
            kwargs={"shift_assignment_id": self.first_employee_shift_assignment.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
