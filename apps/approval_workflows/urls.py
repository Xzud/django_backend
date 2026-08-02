from django.urls import path
from apps.approval_workflows.views import (
    ApprovalWorkflowView,
    ApprovalWorkflowDetailView,
)

urlpatterns = [
    path(
        "",
        view=ApprovalWorkflowView.as_view(),
        name="approval_workflow_list",
    ),
    path(
        "<int:workflow_id>/",
        view=ApprovalWorkflowDetailView.as_view(),
        name="approval_workflow_detail",
    ),
]
