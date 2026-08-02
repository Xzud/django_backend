from django.db import models

# Create your models here.

# approval_tasks
# ---------------
# id
# approval_instance_id
# approval_step_id
# approver_id
# status (
# WAITING
# PENDING
# APPROVED
# REJECTED
# SKIPPED
# )
# sequence # maybe not needed?
# assigned_at
# acted_at
# remarks
# delegated_from_id # When current assigner is unavailable, approval is delegated
# created_at
# updated_at


class ApprovalTask(models.Model):
    class ApprovalTaskStatus(models.TextChoices):
        WAITING = "WAITING", "Waiting"
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        SKIPPED = "SKIPPED", "Skipped"

    approval_instance_id = models.ForeignKey(
        "approval_instances.ApprovalInstance", on_delete=models.CASCADE
    )
    approval_step_id = models.ForeignKey(
        "approval_steps.ApprovalStep", on_delete=models.CASCADE
    )
    approver_id = models.ForeignKey(
        "employees.Employee", on_delete=models.CASCADE, related_name="approved_tasks"
    )
    status = models.CharField(
        max_length=10, choices=ApprovalTaskStatus.choices, default="WAITING"
    )
    sequence = models.IntegerField(null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    acted_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    delegated_from_id = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="delegated_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ApprovalTask {self.id} - Status: {self.status}"
