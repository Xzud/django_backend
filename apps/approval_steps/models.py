from django.db import models

# Create your models here.
# approval_steps
# --------------
# id
# workflow
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
# department
# position
# employee
# is_required
# can_skip
# created_at
# updated_at


class ApprovalStep(models.Model):
    class ApproverType(models.TextChoices):
        DIRECT_SUPERVISOR = "DIRECT_SUPERVISOR", "Direct Supervisor"
        SUPERVISOR_LEVEL = "SUPERVISOR_LEVEL", "Supervisor Level"
        ROLE = "ROLE", "Role"
        DEPARTMENT_ROLE = "DEPARTMENT_ROLE", "Department Role"
        SPECIFIC_EMPLOYEE = "SPECIFIC_EMPLOYEE", "Specific Employee"

    workflow = models.ForeignKey(
        "approval_workflows.ApprovalWorkflow",
        on_delete=models.CASCADE,
        related_name="approval_steps",
    )
    step_order = models.IntegerField()
    name = models.CharField(max_length=255)
    approver_type = models.CharField(max_length=255, choices=ApproverType.choices)
    supervisor_level = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="department_approval_steps",
    )
    position = models.ForeignKey(
        "positions.EmployeePosition",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="position_approval_steps",
    )
    employee = models.ForeignKey(
        "employees.Employee",
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
