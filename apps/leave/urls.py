from rest_framework.urls import path

from apps.leave.views import (
    ApproveLeaveView,
    LeaveView,
    LeaveWithIDView,
    RejectLeaveView,
)

urlpatterns = [
    path("", view=LeaveView.as_view(), name="leaves"),
    path("<int:leave_id>/", view=LeaveWithIDView.as_view(), name="leave_with_id"),
    path(
        "<int:leave_id>/approve/", view=ApproveLeaveView.as_view(), name="approve_leave"
    ),
    path("<int:leave_id>/reject/", view=RejectLeaveView.as_view(), name="reject_leave"),
]
