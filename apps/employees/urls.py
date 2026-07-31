from rest_framework.urls import path
from apps.employees.views import (
    EmployeeView,
    EmployeeWithIDView,
    get_active_employee_shift,
    get_employee_shift,
)

urlpatterns = [
    path("", view=EmployeeView.as_view(), name="employees"),
    path("<int:employee_id>/", view=EmployeeWithIDView.as_view(), name="edit_employee"),
    path(
        "<int:employee_id>/shift-assignment/",
        view=get_employee_shift,
        name="employe_shift",
    ),
    path(
        "<int:employee_id>/shift-assignment/active/",
        view=get_active_employee_shift,
        name="active_employe_shift",
    ),
]
