from django.core.management.base import BaseCommand

from tbot.main import main


class Command(BaseCommand):
    help = "Start polling"

    def handle(self, *args, **options):
        main()
