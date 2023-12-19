from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a superuser if it does not already exist'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Specify the username')
        parser.add_argument('--email', type=str, help='Specify the email address')
        parser.add_argument('--password', type=str, help='Specify the password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists'))
