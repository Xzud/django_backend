from django.db import models

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


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('hr', 'HR'), ('manager', 'Manager'), ('employee', 'Employee')], default='employee')

    def __str__(self):
        return self.username