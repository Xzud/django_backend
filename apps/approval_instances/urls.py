from django.urls import path

from apps.approval_instances.views import (
    ApprovalInstanceDetailView,
    ApprovalInstanceView,
)

urlpatterns = [
    path("", view=ApprovalInstanceView.as_view(), name="approval_instance_list"),
    path(
        "<int:approval_id>/",
        view=ApprovalInstanceDetailView.as_view(),
        name="approval_instance_detail",
    ),
]
