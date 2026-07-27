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
        url = reverse("employees")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_employee(self):
        url = reverse("edit_employee", kwargs={"employee_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_employee(self):
        url = reverse("employees")

        user = User.objects.create_user(
            username="testuser1",
            email="testuser@example.com",
            password="testuserpassword",
            role="employee",
        )

        employee_detail = {
            "employee_number": "EMP002",
            "user": user.id,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "hire_date": "2024-01-02",
            "status": "active",
        }

        response = self.client.post(url, employee_detail)

        self.assertEqual(response.data["id"], 2)
        self.assertEqual(user.id, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], employee_detail["first_name"])
        self.assertEqual(response.data["user"], employee_detail["user"])

    def test_put_employee(self):
        url = reverse("edit_employee", kwargs={"employee_id": 1})

        employee_detail = {
            "employee_number": "EMP001",
            "user": 1,
            "first_name": "Jerry",
            "last_name": "Doe",
            "email": "jerry.doe@example.com",
            "hire_date": "2024-01-01",
            "status": "active",
        }

        response = self.client.put(url, employee_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["first_name"], self.employee.first_name)
        self.assertEqual(response.data["first_name"], employee_detail["first_name"])

    def test_patch_employee(self):
        url = reverse("edit_employee", kwargs={"employee_id": 1})

        employee_detail = {"email": "jerry@example.com"}

        response = self.client.patch(url, employee_detail)

        self.assertEqual(employee_detail["email"], response.data["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_employee(self):
        url = reverse("edit_employee", kwargs={"employee_id": 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # TODO add another assertion to check that employees are now empty
