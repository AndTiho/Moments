from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""

    about_me = models.CharField(max_length=150, verbose_name="О себе", blank=True)
