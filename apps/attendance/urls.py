from rest_framework.urlpatterns import path
from .views import (
    AttendanceClockOutView,
    AttendanceView,
    AttendanceClockInView,
    AttendanceViewID,
)

urlpatterns = [
    path("", view=AttendanceView.as_view(), name="attendance"),
    path("clock-in/", view=AttendanceClockInView.as_view(), name="clock_in"),
    path(
        "clock-out/",
        view=AttendanceClockOutView.as_view(),
        name="clock_out",
    ),
    path(
        "<int:employee_id>/",
        view=AttendanceViewID.as_view(),
        name="employee_attendance",
    ),
]
