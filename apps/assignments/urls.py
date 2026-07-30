from django.urls import path
from . import views

urlpatterns = [
    path("", views.ESA_ListView.as_view(), name="assignment_list"),
    path("create/", views.ESA_CreateView.as_view(), name="create_assignment"),
    path(
        "<int:shift_assignment_id>/",
        views.ESA_DetailView.as_view(),
        name="assignment_detail",
    ),
    path(
        "<int:shift_assignment_id>/edit/",
        views.ESA_EditView.as_view(),
        name="edit_assignment",
    ),
    # /employee/{employee_id}/shift-assignment/ -> current active shift assignment
]
