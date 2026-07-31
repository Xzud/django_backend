from django.db.models import Q
from django.shortcuts import render

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from apps.assignments.models import EmployeeShiftAssignment
from apps.assignments.serializers import EmployeeShiftAssignmentSerializer
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
    def get(self, request):
        """Get /employees"""
        employees = self.service.fetch_employees()
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    permission_classes = [IsAuthenticated]

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


# /employee/{employee_id}/shift-assignment/
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_employee_shift(request, employee_id):
    assignment = EmployeeShiftAssignment.objects.filter(
        employee_id=employee_id
    ).order_by("-effective_from")
    serializer = EmployeeShiftAssignmentSerializer(assignment, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# /employee/{employee_id}/shift-assignment/
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_active_employee_shift(request, employee_id):
    today = timezone.localdate()
    # TODO create a service to get the active shift
    assignment = (
        EmployeeShiftAssignment.objects.select_related(
            "employee", "shift", "assigned_by"
        )
        .filter(
            employee_id=employee_id,
            effective_from__lte=today,
        )
        .filter(Q(effective_to__gt=today) | Q(effective_to__isnull=True))
        .order_by("-effective_from")
        .first()
    )

    # NOTE edge case: if there is no assignment specified
    serializer = EmployeeShiftAssignmentSerializer(assignment)
    return Response(serializer.data, status=status.HTTP_200_OK)
