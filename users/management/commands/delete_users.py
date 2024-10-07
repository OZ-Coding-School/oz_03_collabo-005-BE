from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        one_week_ago = timezone.localtime((timezone.now() - timezone.timedelta(days=7))).date()
        users = CustomUser.objects.filter(deleted_at__lte=one_week_ago)
        users.delete()
        self.stdout.write(self.style.SUCCESS("Successfully deleted users"))
