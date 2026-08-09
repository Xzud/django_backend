from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from .models import ApprovalInstance
from .serializers import ApprovalInstanceSerializer

# Create your views here.


# TODO this will become a manual assignation of approval tasks with the guidance of approval steps
# NOTE this might need a huge refactoring, still considering
@api_view["GET"]
@permission_classes[IsAuthenticated]
def get_approval_instance(request):
    pass


def create_approval_instance(request):
    pass
