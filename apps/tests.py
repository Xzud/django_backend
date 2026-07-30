from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from apps.employees.models import Employee


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

        self.client.force_authenticate(user=self.user)
