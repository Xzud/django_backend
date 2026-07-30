from django.shortcuts import get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from .models import EmployeeShift
from .serializers import EmployeeShiftSerializer

# Create your views here.


class EmplyoeeShiftView(GenericAPIView):
    serializer_class = EmployeeShiftSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shifts = EmployeeShift.objects.all()
        serializer = self.get_serializer(shifts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            shift = serializer.save()
            return Response(
                self.get_serializer(shift).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class EmployeeShiftDeleteView(GenericAPIView):
    serializer_class = EmployeeShiftSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, shift_id):
        shift = get_object_or_404(EmployeeShift, pk=shift_id)
        shift.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
