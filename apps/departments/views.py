from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.departments.models import Department
from apps.departments.serializers import DepartmentSerializer

# Create your views here.

# GET    /departments
# GET    /departments/{id}
# POST   /departments
# PUT    /departments/{id}
# DELETE /departments/{id}


class DepartmentView(APIView):
    def get(self, request):
        try:
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response(
                serializer.errors,
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)

        if serializer.is_valid():
            department = serializer.save()
            return Response(
                DepartmentSerializer(department).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentWithIDView(APIView):
    def get(self, request, department_id):
        try:
            if department_id:
                department = Department.objects.get(id=department_id)
                serializer = DepartmentSerializer(department)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response(
                serializer.errors,
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, department_id):
        department = Department.objects.get(id=department_id)

        serializer = DepartmentSerializer(department, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, department_id):
        department = Department.objects.get(id=department_id)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
