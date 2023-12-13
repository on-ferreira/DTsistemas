from django.core.management.base import BaseCommand
from django.utils import timezone
from background_task.models import Task

class Command(BaseCommand):
    help = 'Clean or delete scheduled tasks.'

    def handle(self, *args, **options):
        """ Clean all tasks previously scheduled."""
        Task.objects.filter(run_at__lt=timezone.now()).delete()

        self.stdout.write(self.style.SUCCESS('Successfully cleaned tasks.'))