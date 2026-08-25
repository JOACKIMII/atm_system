from django.core.management.base import BaseCommand
from atm.models import Account


class Command(BaseCommand):
    help = "Create or update ATM accounts"

    def handle(self, *args, **options):

        accounts = [
            {
                "account_number": "01",
                "full_name": "RAYMOND MTEMBEI",
                "pin": "1234",
                "balance": 100000,
            },
        ]

        for data in accounts:

            account, created = Account.objects.get_or_create(
                account_number=data["account_number"],
                defaults={
                    "full_name": data["full_name"],
                    "balance": data["balance"],
                },
            )

            account.full_name = data["full_name"]
            account.balance = data["balance"]

            # Save PIN using the model's hashing method
            account.set_pin(data["pin"])
            account.save()

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Account created: {account.account_number}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Account updated: {account.account_number}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "ATM accounts setup completed successfully."
            )
        )