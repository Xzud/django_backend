from django.urls import path
from .views import ApprovalStepView, ApprovalStepDetailView

urlpatterns = [
    path("", view=ApprovalStepView.as_view(), name="approval_step_list"),
    path(
        "<int:step_id>/",
        view=ApprovalStepDetailView.as_view(),
        name="approval_step_detail",
    ),
]
