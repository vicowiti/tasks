from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create an initial superuser if it does not exist."

    def handle(self, *args, **options):
        User = get_user_model()

        username = "admin@taskio"
        email = "admin@example.com"
        password = "Admin123!"

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Superuser already exists"))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
