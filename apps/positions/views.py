from django.shortcuts import get_object_or_404, render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .models import EmployeePosition
from .serializers import EmployeePositionSerializer


# Create your views here.
class EmployeePositionlistCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeePositionSerializer

    def get(self, request):
        position = EmployeePosition.objects.all()
        serializer = self.get_serializer(position, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            position = serializer.save()
            return Response(
                self.get_serializer(position).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeePositionDetailView(GenericAPIView):
    serializer_class = EmployeePositionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, position_id):
        position = get_object_or_404(EmployeePosition, pk=position_id)

        return Response(self.get_serializer(position).data, status=status.HTTP_200_OK)

    def patch(self, request, position_id):
        position = get_object_or_404(EmployeePosition, pk=position_id)
        serializer = self.get_serializer(position, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, position_id):
        position = get_object_or_404(EmployeePosition, pk=position_id)
        position.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
