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
            created_by_id=self.owner.id,
        )

    def test_get_all_approval_workflows(self):
        pass

    def test_get_one_approval_workflow(self):
        pass

    def test_create_approval_workflow(self):
        url = reverse("approval_workflow_list")
        new_workflow = {
            "name": "Leave Workflow",
            "request_type": ApprovalWorkflow.ApprovalWorkflowType.PROMOTION,
        }

        response = self.client.post(url, new_workflow)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_approval_workflow(self):
        pass

    def test_delete_approval_workflow(self):
        pass
