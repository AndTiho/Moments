from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Кастомная модель пользователя"""

    about_me = models.CharField(max_length=150, verbose_name="О себе", blank=True)
