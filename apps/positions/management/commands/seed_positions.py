from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

from apps.positions.models import EmployeePosition


class Command(BaseCommand):
    help = "Seed employees with positions"

    def handle(self, *args, **options):
        employees = Employee.objects.all()

        positions = [
            {"name": "IT Administrator", "level": 20},
            {"name": "Staff", "level": 10},
            {"name": "Manager", "level": 100},
        ]

        for position in positions:
            position["object"] = EmployeePosition.objects.get_or_create(
                name=position["name"], level=position["level"]
            )

        print(f"positions: {positions}")

        for i, employee in enumerate(employees):
            if not employee.position:
                position, _ = positions[i%3]["object"]
                employee.position = position
                employee.save()

        