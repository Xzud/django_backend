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
        self.service = EmployeeService()

    def get(self, request, employee_id=None):
        """Get /employees or /employees/{id}"""
        try:
            if employee_id:
                employee = self.service.fetch_employee_with_relations_by_id(employee_id)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                employees = self.service.fetch_employees()
                serializer = EmployeeSerializer(employees, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found")

    def post(self, request):
        pass
