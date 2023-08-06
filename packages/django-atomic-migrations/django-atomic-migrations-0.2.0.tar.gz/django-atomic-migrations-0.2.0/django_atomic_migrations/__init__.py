# -* encoding: utf-8 *-

name = "django_atomic_migrations"

from django.apps.config import AppConfig

def _monkey_patch():
    from django.db.migrations.recorder import MigrationRecorder

    MigrationRecorder.Migration._meta.unique_together = (('app', 'name'),)


class AtomicMigrations(AppConfig):
    name = "django_atomic_migrations"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._patched = False

    def ready(self) -> None:
        if not self._patched:
            _monkey_patch()
            self._patched = True
