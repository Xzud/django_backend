from rest_framework.urls import path
from apps.employees.views import EmployeeView, EmployeeWithIDView

urlpatterns = [
    path("", view=EmployeeView.as_view(), name="employees"),
    path("<int:employee_id>/", view=EmployeeWithIDView.as_view(), name="edit_employee"),
    # /employee/{employee_id}/shift-assignment/ -> current active shift assignment
]
