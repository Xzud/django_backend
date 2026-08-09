from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Seed all application data"

    def handle(self, *args, **kwargs):
        call_command("seed_employees")
        call_command("seed_departments")

        self.stdout.write(self.style.SUCCESS("All seed data created successfully."))
