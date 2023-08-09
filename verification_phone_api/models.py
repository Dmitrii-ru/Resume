from django.db import models

from django.db import models


class CustomUser(models.Model):
    phone_number = models.CharField(max_length=16, unique=True)
    invite = models.CharField(max_length=6, null=True, blank=True)
    self_invite = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=False)

