from rest_framework.urlpatterns import path
from .views import DepartmentView

urlpatterns = [
    path("", view=DepartmentView.as_view(), name="departments"),
    path("<int:department_id>", view=DepartmentView.as_view(), name="department_id"),
]
