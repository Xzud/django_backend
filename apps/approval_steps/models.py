from django.db import models

# Create your models here.
# approval_steps
# --------------
# id
# workflow_id
# step_order
# name
#     (Human-readable label)
# approver_type (
#     DIRECT_SUPERVISOR
#     SUPERVISOR_LEVEL
#     ROLE
#     DEPARTMENT_ROLE
#     SPECIFIC_EMPLOYEE
# )
# supervisor_level
# department_id
# role_id
# employee_id
# is_required
# can_skip
# created_at
# updated_at


class ApprovalStep(models.Model):
    workflow_id = models.ForeignKey(
        "approval_workflows.ApprovalWorkflow",
        on_delete=models.CASCADE,
        related_name="approval_steps",
    )
    step_order = models.IntegerField()
    name = models.CharField(max_length=255)
    approver_type = models.CharField(max_length=255)
    supervisor_level = models.IntegerField(blank=True, null=True)
    department_id = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="department_approval_steps",
    )
    position_id = models.ForeignKey(
        "positions.Position",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="position_approval_steps",
    )
    employee_id = models.ForeignKey(
        "positions.Position",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="employee_approval_steps",
    )
    is_required = models.BooleanField(default=True)
    can_skip = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
