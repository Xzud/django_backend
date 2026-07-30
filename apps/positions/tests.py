from django.urls import reverse
from rest_framework import status
from apps.positions.models import EmployeePosition
from apps.tests import CustomAPITestCase

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data), 0)

    def test_fetch_position_detail(self):
        url = reverse(
            "position-detail", kwargs={"position_id": self.employee.position.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.employee.position.name)

    def test_add_position(self):
        url = reverse("position-list")
        position_details = {
            "name": "HR Department",
            "description": "This department handles Human Resrouces",
        }

        response = self.client.post(url, position_details)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], position_details["name"])
        self.assertEqual(response.data["description"], position_details["description"])

    def test_patch_position(self):
        url = reverse(
            "position-detail", kwargs={"position_id": self.employee.position.id}
        )
        position_details = {"description": "This department handles IT Related tasks"}
        response = self.client.patch(url, position_details)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], position_details["description"])

    def test_delete_position(self):
        url = reverse(
            "position-detail", kwargs={"position_id": self.employee.position.id}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_found_position(self):
        url = reverse("position-detail", kwargs={"position_id": 99})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
