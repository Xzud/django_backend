from rest_framework.urlpatterns import path
from .views import DepartmentView, DepartmentWithIDView

urlpatterns = [
    path("", view=DepartmentView.as_view(), name="departments"),
    path(
        "<int:department_id>", view=DepartmentWithIDView.as_view(), name="department_id"
    ),
]
