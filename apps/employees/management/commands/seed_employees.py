from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from apps.employees.models import Employee
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Seed the employee and users table"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of employee users to create"
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options["count"]

        total_employees = Employee.objects.count()

        try:
            with transaction.atomic():
                for i in range(1, count + 1):
                    employee_user = get_user_model().objects.create_user(
                        username=fake.user_name(),
                        email=fake.email(),
                        password="example@123",
                    )

                    Employee.objects.create(
                        employee_number=f"EMP00{total_employees + i:05d}",
                        user=employee_user,
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=employee_user.email,
                        hire_date="2024-01-01",
                        status="active",
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Seeding failed. All changes were rolled back. \n{e}")
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} users!"))
