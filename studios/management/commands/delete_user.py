from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from studios.models import Booking


class Command(BaseCommand):
    help = "Debug command to delete a user and cascade delete bookings. Not used by UI."

    def add_arguments(self, parser):
        parser.add_argument('--login', type=str, required=True)

    def handle(self, *args, **options):
        login = options['login']
        User = get_user_model()
        user = User.objects.get(login=login)
        Booking.objects.filter(user=user).count()
        user.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted user {login}"))

