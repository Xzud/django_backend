from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import EmployeeDayOff
from .serializers import EmployeeDayOffSerializer

# Create your views here.


class EmployeeDayOffView(GenericAPIView):
    serializer_class = EmployeeDayOffSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dayoff = EmployeeDayOff.objects.all()
        serializer = self.get_serializer(dayoff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            dayoff = serializer.save()
            return Response(self.get_serializer(dayoff).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDayOffDeleteView(GenericAPIView):
    serializer_class = EmployeeDayOffSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, dayoff_id):
        dayoff = get_object_or_404(EmployeeDayOff, pk=dayoff_id)
        dayoff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
