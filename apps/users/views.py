from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer

# Create your views here.


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_auth(request):
    return Response({"message": "Authenticated."}, status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def auth_me(request):
    employee = Employee.objects.select_related("user", "department").get(
        user_id=request.user.id
    )

    print(employee)
    serializer = EmployeeSerializer(employee)

    return Response(
        {
            "employee": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
