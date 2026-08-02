from django.db import models

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

# Create your models here.
# approval_instances
# ------------------
# id
# workflow_id
# request_content_type_id # Lead to different request object types (e.g. LeaveRequest, ExpenseRequest, etc.)
# request_object_id
# requester_id
# status (
# DRAFT
# IN_PROGRESS
# APPROVED
# REJECTED
# CANCELLED
# )
# current_step_id
# started_at
# completed_at
# created_at
# updated_at


# TODO continue this with the proper polymporphic relationship for request_content_type_id and request_object_id
class ApprovalInstance(models.Model):
    workflow_id = models.ForeignKey(
        "approval_workflows.ApprovalWorkflow",
        on_delete=models.CASCADE,
        related_name="approval_instances",
    )
    request_content_type_id = models.IntegerField()
    request_object_id = models.IntegerField()
    requester_id = models.IntegerField()
    status = models.CharField(max_length=255)
    current_step_id = models.ForeignKey(
        "approval_steps.ApprovalStep",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="current_approval_instances",
    )
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ApprovalInstance {self.id} - Workflow {self.workflow_id}"
