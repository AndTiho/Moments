from django.conf import settings
from django.db import models


class Moment(models.Model):
    """Модель для создания настоящего момента"""

    title = models.CharField(
        max_length=50,
        verbose_name="Название момента",
        help_text="Подарите моменту название",
    )
    details = models.TextField(
        verbose_name="Описание момента",
        help_text="Опишите момент",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="moments/%Y/%m/%d/",
        verbose_name="Изображение момента",
        help_text="Загрузите изображение момента",
        blank=True,
        null=True,
    )
    music_url = models.URLField(
        verbose_name="Музыка момента",
        help_text="Вставьте музыкальную ссылку",
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="moments",
    )

    is_public = models.BooleanField(default=False, verbose_name="Публичный момент")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "момент"
        verbose_name_plural = "моменты"
