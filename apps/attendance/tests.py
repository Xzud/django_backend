from django.urls import reverse
from rest_framework import status

from apps.tests import CustomAPITestCase

from .models import Attendance

# Create your tests here.


class Attendancetest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        self.attendance_now = Attendance.objects.create(
            employee=self.employee,
            date="2024-04-01",
            clock_in="2026-07-28T08:00:00Z",
            clock_out="2026-07-28T17:00:00Z",
            status="present",
        )


    def test_fetch_attendances(self):
        url = reverse("attendance")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_employee_attendance(self):
        url = reverse("employee_attendance", kwargs={"employee_id": 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["date"], self.attendance_now.date)
        self.assertEqual(response.data["clock_in"], self.attendance_now.clock_in)
        self.assertEqual(response.data["clock_out"], self.attendance_now.clock_out)
        self.assertEqual(response.data["status"], self.attendance_now.status)

    def test_clock_in(self):
        url = reverse("clock_in")

        response = self.client.post(url, {"employee": self.employee.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["clock_out"], None)

        response = self.client.post(url, {"employee": "asd"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clouck_out(self):
        url = reverse("clock_out", kwargs={"attendance_id": 1})

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["clock_in"], self.attendance_now.clock_in)
        self.assertNotEqual(response.data["clock_out"], None)
