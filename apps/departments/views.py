from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from apps.departments.models import Department
from apps.departments.serializers import DepartmentSerializer

# Create your views here.

# GET    /departments
# GET    /departments/{id}
# POST   /departments
# PUT    /departments/{id}
# DELETE /departments/{id}


class DepartmentView(GenericAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(operation_id="all_departments")
    def get(self, request):
        try:
            departments = Department.objects.all()
            serializer = self.get_serializer(departments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response(
                serializer.errors,
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            department = serializer.save()
            return Response(
                self.get_serializer(department).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentWithIDView(GenericAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(operation_id="single_department")
    def get(self, request, department_id):
        try:
            if department_id:
                department = Department.objects.get(id=department_id)
                serializer = self.get_serializer(department)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response(
                serializer.errors,
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, department_id):
        department = Department.objects.get(id=department_id)

        serializer = self.get_serializer(department, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, department_id):
        department = Department.objects.get(id=department_id)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
