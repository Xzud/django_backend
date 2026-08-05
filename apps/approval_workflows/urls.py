from django.urls import path, include
from apps.approval_steps.views import get_workflow_steps
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
    path(
        "<int:workflow_id>/steps/",
        view=get_workflow_steps,
        name="approval_workflow_steps",
    ),
]
