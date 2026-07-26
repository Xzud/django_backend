from django.db import models

# Create your models here.

# Attendance
# ----------
# id
# employee
# date
# clock_in
# clock_out
# status

class Attendance(models.Model):
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
    date = models.DateField()
    clock_in = models.DateTimeField(blank=True, null=True)
    clock_out = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], default='present')
    