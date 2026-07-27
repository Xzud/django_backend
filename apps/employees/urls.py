from rest_framework.urls import path
from apps.employees.views import EmployeeView

urlpatterns = [
    path("", view=EmployeeView.as_view(), name="employees"),
    path("<int:employee_id>", view=EmployeeView.as_view(), name="edit_employee"),
]
