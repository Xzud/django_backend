from django.urls import path
from apps.approval_tasks.views import ApprovalTaskView, ApprovalTaskDetailsView

urlpatterns = [
    path("", view=ApprovalTaskView.as_view(), name="approval_task_list"),
    path(
        "<int:task_id>/",
        view=ApprovalTaskDetailsView.as_view(),
        name="approval_task_details",
    ),
]
