from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_auth(request):
    return Response({"message": "Authenticated."}, status.HTTP_200_OK)
