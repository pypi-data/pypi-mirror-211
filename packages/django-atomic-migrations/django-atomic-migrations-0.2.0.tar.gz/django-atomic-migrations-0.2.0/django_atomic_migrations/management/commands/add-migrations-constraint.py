from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Adds unique constraint for migrations tracking model"

    def handle(self, **kwargs):
        editor = connection.schema_editor()
        from django.db.migrations.recorder import MigrationRecorder

        with connection.cursor() as cursor:
            cursor.execute(str(editor._create_unique_sql(MigrationRecorder.Migration, ('app', 'name'))))
