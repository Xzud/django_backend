from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.serializers import LoginSerializer
from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer
from .services import AuthenticationService

# Create your views here.

# POST /api/auth/login
# POST /api/auth/refresh
# GET  /api/auth/me

User = get_user_model()


@extend_schema(request=LoginSerializer, responses={200: dict})
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    User login view.
    """

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user_details = AuthenticationService.login(
        request, username=username, password=password
    )

    if user_details is None:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    employee = Employee.objects.select_related("user", "department").get(
        user_id=user_details["id"]
    )
    print(employee)
    serializer = EmployeeSerializer(employee)

    return Response(
        {
            "message": "Login successful.",
            "employee": serializer.data,
            "access_token": user_details["access_token"],
            "refresh_token": user_details["refresh_token"],
        },
        status=status.HTTP_200_OK,
    )
