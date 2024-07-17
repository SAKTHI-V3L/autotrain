# timeseries/management/commands/check_db_connection.py

from django.core.management.base import BaseCommand, CommandError
from django.db import connections

class Command(BaseCommand):
    help = 'Checks database connection'

    def handle(self, *args, **options):
        try:
            with connections['default'].cursor() as cursor:
                self.stdout.write(self.style.SUCCESS('Database connection successful!'))
        except Exception as e:
            raise CommandError('Database connection error: %s' % str(e))
