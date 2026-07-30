from django.test import TestCase
from django.urls import reverse
from apps.positions.models import EmployeePosition
from apps.tests import CustomAPITestCase

from rest_framework.test import APITestCase

# Create your tests here.


class EmployeePositionTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        self.employee.position = EmployeePosition.objects.create(
            name="Web Developer",
        )

    def test_fetch_all_positions(self):
        url = reverse("position-list")
        response = self.client.get(url)

        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
