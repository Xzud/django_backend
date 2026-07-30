from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer
from apps.employees.services import EmployeeService

# Create your views here.

# GET    /employees
# GET    /employees/{id}
# POST   /employees
# PUT    /employees/{id}
# DELETE /employees/{id}


class EmployeeView(GenericAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIX will be removing service
        self.service = EmployeeService()

    @extend_schema(operation_id="all_employees")
    def get(self, request, employee_id=None):
        """Get /employees"""
        try:
            # FIX will be removing service
            employees = self.service.fetch_employees()
            serializer = self.get_serializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            raise NotFound("Employees not found")

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                self.get_serializer(employee).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeWithIDView(GenericAPIView):
    serializer_class = EmployeeSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIX will be removing service
        self.service = EmployeeService()

    @extend_schema(operation_id="single_employee")
    def get(self, request, employee_id):
        """Get /employees/{id}"""
        try:
            # FIX will be removing service
            employee = self.service.fetch_employee_with_relations_by_id(employee_id)
            serializer = self.get_serializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found")

    def put(self, request, employee_id):
        # TODO add test
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, employee_id):
        # TODO add test
        employee = Employee.objects.get(id=employee_id)

        serializer = self.get_serializer(employee, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id):
        # TODO add test
        employee = Employee.objects.get(id=employee_id)
        employee.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
