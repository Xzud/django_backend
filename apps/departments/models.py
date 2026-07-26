from django.db import models

# Create your models here.

# Department
# ----------
# id
# name
# description
# manager


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='managed_departments')

    def __str__(self):
        return self.name