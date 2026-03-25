from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""

    HEADER_NAME_CHOICES = [
        ("username", "Никнэйм"),
        ("name", "Имя"),
    ]

    about_me = models.CharField(max_length=150, verbose_name="О себе", blank=True)
    header_name_preference = models.CharField(
        max_length=20,
        choices=HEADER_NAME_CHOICES,
        default="username",
    )

    @property
    def header_display_name(self):
        if self.header_name_preference == "name" and self.first_name:
            return self.first_name
        return self.username
