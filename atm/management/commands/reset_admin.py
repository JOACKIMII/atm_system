from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Reset the Django admin password"

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            type=str,
            required=True,
            help="New password for the admin user",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        password = options["password"]

        try:
            user = User.objects.get(username="admin")
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("User 'admin' does not exist.")
            )
            return

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Admin password changed successfully."
            )
        )