from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Employee

# Create your tests here.

User = get_user_model()


class EmployeeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password="testpass123",
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
        self.client.force_login(self.user)

    def test_fetch_employees(self):
        url = reverse("employee-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_employee(self):
        url = reverse("employee-detail", kwargs={"employee_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
