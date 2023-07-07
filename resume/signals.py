from .models import Project
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from .cache import delete_cache
import redis

@receiver(post_delete, sender=MyEducation)
def education_post_delete(sender, instance, **kwargs):
    delete_cache(sender._meta.model_name)
@receiver(post_delete, sender=AboutMe)
def education_post_delete(sender, instance, **kwargs):
    delete_cache(sender._meta.model_name)

@receiver(post_delete, sender=Stack)
def education_post_delete(sender, instance, **kwargs):
    delete_cache(sender._meta.model_name)

@receiver(post_delete, sender=Project)
def education_post_delete(sender, instance, **kwargs):
    delete_cache(sender._meta.model_name)

@receiver(post_delete, sender=CardProject)
def education_post_delete(sender, instance, **kwargs):
    delete_cache(sender._meta.model_name)