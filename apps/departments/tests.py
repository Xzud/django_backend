from django.contrib.auth import get_user_model

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.departments.models import Department

# Create your tests here.


class DepartmentTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            role="employee",
        )

        self.department = Department.objects.create(
            name="IT Department",
            description="This department handles IT related tasks.",
        )

        self.client.force_login(self.user)

    def test_get_departments(self):
        url = reverse("departments")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_department_with_id(self):
        url = reverse("department_id", kwargs={"department_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_adding_department(self):
        url = reverse("departments")

        department_details = {
            "name": "HR",
            "description": "This department handles employee related tasks.",
        }

        response = self.client.post(url, department_details)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], department_details["name"])

    def test_edit_department(self):
        url = reverse("department_id", kwargs={"department_id": 1})

        department_details = {
            "name": "IT",
            "description": "This department handles System Administrative, Development, IT Maintenance, Networking, and other IT related work.",
        }

        response = self.client.put(url, department_details)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            department_details["description"], response.data["description"]
        )
        self.assertEqual(department_details["name"], response.data["name"])

    def test_delete_department(self):
        url = reverse("department_id", kwargs={"department_id": 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
