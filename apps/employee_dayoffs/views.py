from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import EmployeeDayOff
from .serializers import EmployeeDayOffSerializer

# Create your views here.


class EmployeeDayOffView(GenericAPIView):

    def get(self, request):
        pass

    def post(self, request):
        pass


class EmployeeDayOffDeleteView(GenericAPIView):
    def delete(self, request, dayoff_id):
        pass
