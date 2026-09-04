
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.employees.models import Employee

class Command(BaseCommand):
    help = "Seed to assign supervisory to employees table"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level", type=int, default=100, help="Assign employees below this level with employees on and above this level"
        )

    def handle(self, *args, **options):
        level = options["level"]

        managers = Employee.objects.select_related("position").filter(position__level__gte=level)
        employees = Employee.objects.select_related("position").filter(position__level__lt=level).filter(supervisor__isnull=True)

        try:
            with transaction.atomic():
                for employee in employees:
                    employee.supervisor = managers[random.randint(0, len(managers)-1)]
                    employee.save()
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error on seeding assigned supervisory for employees. \n Error:{e}")
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Success on seeding assigned supervisory for {len(employees)} employee/s"
            )
        )