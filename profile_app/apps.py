from django.apps import AppConfig
from django.db.models.signals import post_save


class ProfileAppConfig(AppConfig):
    name = 'profile_app'

    def ready(self):
        # # импортируем тут, чтобы избежать круговые импорты
        # from .signals import create_profile
        # from django.contrib.auth.models import User
        # post_save.connect(create_profile, sender=User)
        # # а теперь идём в __init__.py и пишем config

        import profile_app.signals
