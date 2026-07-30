from django.urls import path
from .views import EmployeePositionlistCreateView, EmployeePositionDetailView

urlpatterns = [
    path("", EmployeePositionlistCreateView.as_view(), name="position-list"),
    path(
        "<int:position_id>/",
        EmployeePositionDetailView.as_view(),
        name="position-detail",
    ),
]
