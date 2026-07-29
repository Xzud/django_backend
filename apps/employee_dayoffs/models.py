from django.db import models

# Create your models here.


class EmployeeDayOff(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1, "Monday"
        TUESDAY = 2, "Tuesday"
        WEDNESDAY = 3, "Wednesday"
        THURSDAY = 4, "Thursday"
        FRIDAY = 5, "Friday"
        SATURDAY = 6, "Saturday"
        SUNDAY = 7, "Sunday"

    assignment = models.ForeignKey(
        "employee_shift_assignments.EmployeeShiftAssignment",
        on_delete=models.CASCADE,
        related_name="days_off",
    )
    day_of_week = models.PositiveSmallIntegerField(choices=DayOfWeek.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "day_of_week"],
                name="unique_day_off_per_assignment",
            )
        ]
