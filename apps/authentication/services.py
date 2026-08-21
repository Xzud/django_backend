from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken


def auth_login(request, username, password):
    user = authenticate(request, username=username, password=password)

    if user is None:
        return None

    login(request, user)
    refresh = RefreshToken.for_user(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }


def auth_logout(request):
    logout(request)
