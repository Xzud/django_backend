from django.urls import reverse

from rest_framework import status

from apps.tests import CustomAPITestCase
from apps.approval_workflows.models import ApprovalWorkflow

# Create your tests here.


class ApprovalWorkflowsTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        ApprovalWorkflow.objects.create(
            name="Leave Workflow",
            request_type=ApprovalWorkflow.ApprovalWorkflowType.LEAVE,
            created_by=self.owner,
        )

    def test_get_all_approval_workflows(self):
        url = reverse("approval_workflow_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data), 0)

    def test_get_one_approval_workflow(self):
        url = reverse("approval_workflow_detail", kwargs={"workflow_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data), 0)

    def test_create_approval_workflow(self):
        url = reverse("approval_workflow_list")
        new_workflow = {
            "name": "Promotion Workflow",
            "request_type": ApprovalWorkflow.ApprovalWorkflowType.PROMOTION,
        }

        response = self.client.post(url, new_workflow)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_approval_workflow(self):
        url = reverse("approval_workflow_detail", kwargs={"workflow_id": 1})
        updated_workflow = {
            "description": "This is a workflow template used to guide leave approval chain"
        }
        response = self.client.patch(url, updated_workflow)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], updated_workflow["description"])

    def test_delete_approval_workflow(self):
        url = reverse("approval_workflow_detail", kwargs={"workflow_id": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# TODO need more tests that are for specific queries
