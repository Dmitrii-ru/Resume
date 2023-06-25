from .models import Style, Projects
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Projects)
def created_profile(sender, instance, created, **kwargs):
    if created:

        Style.objects.create(project=instance)
