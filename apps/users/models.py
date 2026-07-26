from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# User
# ----
# id
# username
# email
# password
# role

# Roles:

# Admin
# HR
# Manager
# Employee


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('hr', 'HR'), ('manager', 'Manager'), ('employee', 'Employee')], default='employee')

    def __str__(self):
        return self.username