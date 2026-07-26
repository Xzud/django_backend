from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationService:

    @staticmethod
    def login(request, username, password):
        user = authenticate(username, password)

        if user is None:
            return None

        refresh = RefreshToken.for_user(user)

        return (
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            },
        )
