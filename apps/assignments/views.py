from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .serializers import (
    EmployeeShiftAssignmentSerializer,
    ESA_WriteSerializer,
)
from .models import EmployeeShiftAssignment

# Create your views here.


class ESA_ListView(GenericAPIView):
    serializer_class = EmployeeShiftAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shift_assignments = EmployeeShiftAssignment.objects.select_related(
            "employee", "shift", "assigned_by"
        ).all()

        serializer = self.get_serializer(shift_assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ESA_CreateView(GenericAPIView):
    serializer_class = ESA_WriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            assignment = serializer.save()
            return Response(
                self.get_serializer(assignment).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ESA_DetailView(GenericAPIView):
    serializer_class = EmployeeShiftAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, shift_assignment_id):
        assignment = get_object_or_404(EmployeeShiftAssignment, pk=shift_assignment_id)

        serializer = self.get_serializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, shift_assignment_id):
        assignment = get_object_or_404(EmployeeShiftAssignment, pk=shift_assignment_id)
        assignment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ESA_EditView(GenericAPIView):
    serializer_class = ESA_WriteSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, shift_assignment_id):
        assignment = get_object_or_404(EmployeeShiftAssignment, pk=shift_assignment_id)

        serializer = self.get_serializer(assignment, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view, permission_classes


# /shift-assignment/{shift_assignment_id}/dayoffs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_shift_assignment_dayoffs(request, shift_assignment_id):
    try:
        assignment_with_dayoffs = EmployeeShiftAssignment.objects.prefetch_related(
            "days_off"
        ).get(id=shift_assignment_id)
        serializer = EmployeeShiftAssignmentSerializer(assignment_with_dayoffs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except EmployeeShiftAssignment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
