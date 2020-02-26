from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


# # модель которая отправляет сигнал (User), instance - экземпляр сущности
# def create_profile(sender, instance, **kwargs):
#     try:
#         Profile.objects.get(user_id=instance.id)
#     # except ObjectDoesNotExist:
#     except ObjectDoesNotExist:
#         new_profile = Profile()
#         new_profile.user = instance
#         new_profile.save()
#         # идем дальше в apps.py и подключаемся


# -------------------------------------- либо на замену пользуемся двумя этими :)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
