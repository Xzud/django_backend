from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from apps.departments.models import Department


class Command(BaseCommand):
    help = "Seed the departments table"

    def handle(self, *args, **kwargs):
        fake = Faker()

        default_departments = [
            {"name": "IT", "description": ""},
            {"name": "HR", "description": ""},
            {"name": "Finance", "description": ""},
        ]

        try:
            with transaction.atomic():
                for _, department in enumerate(default_departments):
                    Department.objects.create(
                        name=department["name"], description=department["description"]
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error on seeding departments. \n Error:{e}")
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Success on seeding {len(default_departments)} department/s"
            )
        )

        # NOTE after departments have been seeded, consider using seed_assign_departments to fill seeded employees with appropriate departments
