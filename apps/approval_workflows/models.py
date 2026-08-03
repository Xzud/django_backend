from django.db import models

# Create your models here.


# approval_workflows
# ------------------
# id
# name
# description
# request_type
#     (leave, promotion, purchase, etc.)
# is_active
# created_by_id
# created_at
# updated_at


class ApprovalWorkflow(models.Model):
    class ApprovalWorkflowType(models.TextChoices):
        LEAVE = "leave", "Leave"
        PROMOTION = "promotion", "Promotion"
        PURCHASE = "purchase", "Purchase"
        OTHER = "other", "Other"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    request_type = models.CharField(
        max_length=255, choices=ApprovalWorkflowType.choices
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_approval_workflows",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
