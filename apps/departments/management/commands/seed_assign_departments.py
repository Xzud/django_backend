import random

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from apps.departments.models import Department
from apps.employees.models import Employee


class Command(BaseCommand):
    help = "Seed the departments to assign on employees table"

    def handle(self, *args, **kwargs):
        departments = Department.objects.all()
        employees = Employee.objects.filter(department__isnull=True)

        try:
            with transaction.atomic():
                for _, employee in enumerate(employees):
                    employee.department = departments[random.randint(0, len(departments)-1)]
                    employee.save()

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error on seeding when assigning departments to employees. \n Error:{e}")
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Success on seeding employee assigned department/s"
            )
        )
