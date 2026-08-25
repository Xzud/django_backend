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

    class Status(models.TextChoices):
        PRESENT = "Present", "Present"
        ABSENT = "Absent", "Absent"
        LATE = "Late", "Late"

    employee = models.ForeignKey("employees.Employee", on_delete=models.CASCADE)
    date = models.DateField(null=True)
    clock_in = models.DateTimeField(blank=True, null=True)
    clock_out = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default="present",
    )
