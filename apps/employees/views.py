from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer
from apps.employees.services import EmployeeService

# Create your views here.

# GET    /employees
# GET    /employees/{id}
# POST   /employees
# PUT    /employees/{id}
# DELETE /employees/{id}


class EmployeeView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIX will be removing service
        self.service = EmployeeService()

    def get(self, request, employee_id=None):
        """Get /employees or /employees/{id}"""
        try:
            # FIX will be removing service
            employees = self.service.fetch_employees()
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            raise NotFound("Employees not found")

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeWithIDView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIX will be removing service
        self.service = EmployeeService()

    def get(self, request, employee_id):
        """Get /employees or /employees/{id}"""
        try:
            # FIX will be removing service
            employee = self.service.fetch_employee_with_relations_by_id(employee_id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found")

    def put(self, request, employee_id):
        # TODO add test
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, employee_id):
        # TODO add test
        employee = Employee.objects.get(id=employee_id)

        serializer = EmployeeSerializer(employee, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id):
        # TODO add test
        employee = Employee.objects.get(id=employee_id)
        employee.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
