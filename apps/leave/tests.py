from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.employees.models import Employee
from apps.leave.models import Leave
from apps.tests import CustomAPITestCase

# Create your tests here.


class LeaveTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        self.leave = Leave.objects.create(
            employee=self.employee,
            type="Sick Leave",
            start_date="2026-10-11",
            end_date="2026-10-12",
            reason="Fever and severe indigestion.",
        )

        self.client.force_login(self.user)

    def test_fetch_leaves(self):
        url = reverse("leaves")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_leave_with_id(self):
        url = reverse("leave_with_id", kwargs={"leave_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_leave(self):
        url = reverse("leaves")

        leave_details = {
            "employee": self.employee.id,
            "type": "Maternal Leave",
            "start_date": "2026-11-01",
            "end_date": "2027-02-23",
            "reason": "In labor",
        }

        response = self.client.post(url, leave_details)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["type"], leave_details["type"])
        self.assertEqual(response.data["start_date"], leave_details["start_date"])
        self.assertEqual(response.data["end_date"], leave_details["end_date"])
        self.assertEqual(response.data["reason"], leave_details["reason"])

    def test_approve_leave(self):
        url = reverse("approve_leave", kwargs={"leave_id": 1})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "approved")

    def test_reject_leave(self):
        url = reverse("reject_leave", kwargs={"leave_id": 1})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "rejected")
