from django.core.management import BaseCommand

from materials.models import Course
from users.models import Pays, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_content = [
            {
                'user': User.objects.get_or_create(email="vladik@gmail.com")[0],
                'date': "2024-04-17",
                'course': Course.objects.get_or_create(name="Python")[0],
                'amount': 100000,
                'payment_method': 'card',
            }
        ]
        # User.objects.create(email='vladik@gmail.com')

        Pays.objects.bulk_create(
            [Pays(**payment) for payment in payment_content]
        )

#
# (user=User.objects.get_or_create(email="vlad@gmail.com"),
# amount = payment["fields"]["amount"],
# date = payment["fields"]["date"],
# course = payment["fields"]["course"],
# payment_method = payment["fields"]["payment_method"])
