from django.urls import reverse
from urllib.parse import urlencode

from rest_framework import status

from apps.departments.models import Department
from apps.tests import CustomAPITestCase

from apps.approval_workflows.models import ApprovalWorkflow
from apps.approval_steps.models import ApprovalStep

# Create your tests here.


class ApprovalStepTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        leave_workflow = ApprovalWorkflow.objects.create(
            name="Leave Workflow",
            request_type=ApprovalWorkflow.ApprovalWorkflowType.LEAVE,
            created_by=self.owner,
        )

        promotion_workflow = ApprovalWorkflow.objects.create(
            name="Promotion Workflow",
            request_type=ApprovalWorkflow.ApprovalWorkflowType.PROMOTION,
            created_by=self.owner,
        )

        self.promotion_workflow_step_1 = ApprovalStep.objects.create(
            workflow=promotion_workflow,
            step_order=1,
            name="CEO Promotion Approval",
            approver_type=ApprovalStep.ApproverType.SPECIFIC_EMPLOYEE,
            employee=self.owner,
        )

        self.leave_workflow_step_1 = ApprovalStep.objects.create(
            workflow=leave_workflow,
            step_order=1,
            name="Supervisor Approval Step",
            approver_type=ApprovalStep.ApproverType.DIRECT_SUPERVISOR,
            supervisor_level=1,
        )

    def test_get_all_workflow_steps(self):
        url = reverse("approval_step_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_steps_of_workflow(self):
        url = reverse("approval_workflow_steps", kwargs={"workflow_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [step["name"] for step in response.data]
        self.assertIn(self.leave_workflow_step_1.name, names)
        self.assertNotIn(self.promotion_workflow_step_1.name, names)

    def test_get_step_from_id(self):
        url = reverse("approval_step_detail", kwargs={"step_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_workflow_step(self):
        url = reverse("approval_step_list")
        hr_department = Department.objects.create(name="HR Department")

        new_step_details = {
            "workflow": 1,
            "name": "HR Approval",
            "step_order": 2,
            "approver_type": ApprovalStep.ApproverType.DEPARTMENT_ROLE,
            "department": hr_department.id,
        }

        response = self.client.post(url, new_step_details)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["department"], new_step_details["department"])

    def test_edit_workflow_step(self):
        url = reverse("approval_step_detail", kwargs={"step_id": 1})
        new_step_details = {"name": "Supervisor Approval"}
        response = self.client.patch(url, new_step_details)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_step_details["name"])

    def test_delete_workflow_step(self):
        url = reverse("approval_step_detail", kwargs={"step_id": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
