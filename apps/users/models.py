from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""

    HEADER_NAME_CHOICES = [
        ("username", "Никнэйм"),
        ("name", "Имя"),
    ]

    email = models.EmailField(unique=True)
    about_me = models.CharField(max_length=150, verbose_name="О себе", blank=True)
    header_name_preference = models.CharField(
        max_length=20,
        choices=HEADER_NAME_CHOICES,
        default="username",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def header_display_name(self):
        """Для выбора пользователю какое имя высвечивать при заходе на сайт"""
        if self.header_name_preference == "name" and self.first_name:
            return self.first_name
        return self.username
