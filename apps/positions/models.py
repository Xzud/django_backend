from django.db import models

# Create your models here.


# Position Level
# 1000 - CEO / Owner
# 900 - Director
# 200 - Department Head
# 100 - Managers
# 50 - Supervisors
# 30 - Senior Employee
# 10 - Normal Employee
# 1 - Interns


class EmployeePosition(models.Model):
    name = models.CharField(min=20, max=100)
    description = models.TextField(blank=True, null=True)
    level = models.PositiveIntegerField(default=10)
