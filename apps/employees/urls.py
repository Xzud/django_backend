from rest_framework.urls import path
from apps.employees.views import EmployeeView

urlpatterns = [
    path("", view=EmployeeView.as_view(), name="employee-list"),
    path("<int:employee_id>", EmployeeView.as_view(), name="employee-detail")
]
