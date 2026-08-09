from django.db import models

# Create your models here.


# Leave
# -----
# id
# employee
# type
# start_date
# end_date
# reason
# status
# approved_by


class Leave(models.Model):
    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        related_name="employee_on_leave",
        null=True,
        blank=True,
    )
    type = models.CharField(
        max_length=100
    )  # Sick Leave, Maternal Leave, Paternal Leave, Personal Leave, Paid Leave, Vacation Leave, Others
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
