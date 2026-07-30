from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.EmplyoeeShiftView.as_view(), name="employee_shifts"),
    path(
        "<int:shift_id>/",
        view=views.EmployeeShiftDeleteView.as_view(),
        name="delete_employee_shift",
    ),
]
