from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.EmployeeDayOffView.as_view(), name="employee_dayoffs"),
    path(
        "<int:dayoff_id>/",
        view=views.EmployeeDayOffDeleteView.as_view(),
        name="delete_employee_dayoff",
    ),
]
