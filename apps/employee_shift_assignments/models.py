from django.db import models

# Create your models here.

# employee_shift_assignments
# --------------------------
# id
# employee_id
# shift_id
# effective_from
# effective_to
# assigned_by


class EmployeeShiftAssignment(models.Model):
    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="shift_assignments",
    )
    shift = models.ForeignKey(
        "shifts.EmployeeShift",
        on_delete=models.SET_NULL,
        null=True,
        related_name="employee_assignments",
    )
    effective_from = models.DateField()
    effective_to = models.DateField(blank=True, null=True)
    assigned_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_shifts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
