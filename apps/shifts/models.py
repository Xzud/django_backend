from django.db import models

# Create your models here.

# shifts
# ------
# id
# name
# start_time
# end_time
# break_minutes
# grace_period
# is_night_shift


class ShiftType(models.TextChoices):
    FIXED = "FIXED", "Fixed Schedule"
    FLEX_DAILY = "FLEX_DAILY", "Flexible Daily Hours"
    FLEX_WEEKLY = "FLEX_WEEKLY", "Flexible Weekly Hours"


class EmployeeShift(models.Model):

    name = models.CharField(max_length=50, unique=True)

    shift_type = models.CharField(
        max_length=20, choices=ShiftType.choices, default=ShiftType.FIXED
    )

    # If working time is fixed
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    # If working time is daily flex
    required_hours_per_day = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    # If working time is weekly flex
    required_hours_per_week = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    break_minutes = models.PositiveSmallIntegerField(default=60)
    grace_period_minute = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_ate = models.DateTimeField(auto_now=True)
