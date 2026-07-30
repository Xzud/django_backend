from django.db import models
from django.conf import settings

# Create your models here.

# Employee
# ---------
# id
# user
# employee_number
# first_name
# last_name
# email
# phone
# birth_date
# hire_date
# department
# position
# status
# created_at
# updated_at


class Employee(models.Model):
    employee_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="employee_detail",
    )
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="employees",
    )
    # supervisor
    # team_leader
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    hire_date = models.DateField()
    position = models.ForeignKey(
        "positions.EmployeePosition",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="position_employees",
    )
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        default="active",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_number})"
