from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.

# POST /api/auth/login
# POST /api/auth/refresh
# GET  /api/auth/me


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login view.
    """

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'detail': 'Username and password are required.'},status=status.HTTP_400_BAD_REQUEST,
        )


    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response(
            {'detail':'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )


    return Response(
        {'message' : 'Login successful.', 
         'user': {'id': user.id, 'username': user.username, 'email': 'user.email', 'role': user.role}
        },
        status=status.HTTP_200_OK,
    )