from django.test import TestCase

from rest_framework import status

from apps.tests import CustomAPITestCase

# Create your tests here.


class ApprovalStepTest(CustomAPITestCase):
    def setUp(self):
        return super().setUp()

    def test_get_all_workflow_steps(self):
        pass

    def test_get_steps_of_workflow(self):
        pass

    def test_get_step_from_id(self):
        pass

    def test_create_workflow_step(self):
        pass

    def test_edit_workflow_step(self):
        pass

    def test_delete_workflow_step(self):
        pass
