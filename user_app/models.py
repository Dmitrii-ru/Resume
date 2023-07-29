from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField('Фото пользователя', default='default_user.png', upload_to='user_images')
    create = models.DateTimeField(auto_now_add=True)
    reset_password = models.BooleanField(default=False)

    def __str__(self):
        return f"Профайл пользователя {self.user.username}"

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)
        if image.height > 100 or image.width > 100:
            resize = (100, 100)
            image.thumbnail(resize)

            image.save(self.img.path)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
