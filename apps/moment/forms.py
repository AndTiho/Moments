from io import BytesIO
import os

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from apps.moment.models import Moment


class MomentForm(forms.ModelForm):
    """Форма для модели Момент"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self._old_image = self.instance.image
        else:
            self._old_image = None

    image_clear = forms.BooleanField(required=False)

    class Meta:
        model = Moment
        fields = ("title", "details", "image", "music_url", "is_public")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "Например: Тёплый ветер и чай с мятой",
            }),
            "details": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full rounded-2xl min-h-40",
                "placeholder": "Что ты чувствуешь прямо сейчас?",
            }),
            "image": forms.FileInput(attrs={
                "class": "file-input file-input-bordered w-full rounded-2xl",
                "id": "image-input",
                "accept": "image/*",
            }),
            "music_url": forms.URLInput(attrs={
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "https://...",
            }),
            "is_public": forms.CheckboxInput(attrs={
                "class": "toggle toggle-primary",
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            return image

        # Если новая картинка не загружалась, ничего не трогаем
        if "image" not in self.files:
            return image

        if image.size > 10 * 1024 * 1024:
            raise ValidationError("Картинка слишком большая (максимум 10 MB)")

        try:
            img = Image.open(image)
            img.verify()
        except Exception:
            raise ValidationError("Файл не является корректным изображением")

        image.seek(0)
        img = Image.open(image)

        width, height = img.size

        if width < 400 or height < 400:
            raise ValidationError("Картинка слишком маленькая (минимум 400x400)")

        if width > 8000 or height > 8000:
            raise ValidationError("Изображение слишком большое")

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        max_size = 1600
        if max(width, height) > max_size:
            img.thumbnail((max_size, max_size))

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        original_name = os.path.splitext(image.name)[0]
        new_name = f"{original_name}.jpg"

        return InMemoryUploadedFile(
            file=buffer,
            field_name="image",
            name=new_name,
            content_type="image/jpeg",
            size=buffer.getbuffer().nbytes,
            charset=None,
        )

    def clean(self):
        """Общая проверка на то, что должно быть заполнено хотя бы одно из полей"""
        cleaned_data = super().clean()

        details = cleaned_data.get("details")
        image = cleaned_data.get("image")
        music_url = cleaned_data.get("music_url")

        if not details and not image and not music_url:
            raise forms.ValidationError(
                "Момент не может быть пустым (заполните одно из: описание/изображение/музыка)"
            )

        return cleaned_data

    def save(self, commit=True):
        old_image = self._old_image.name if self._old_image else None
        uploaded_new_image = "image" in self.files

        instance = super().save(commit=False)

        if self.cleaned_data.get("image_clear"):
            instance.image = None

        new_image = instance.image.name if instance.image else None

        if commit:
            instance.save()
            self.save_m2m()

        if old_image and not new_image:
            self._old_image.delete(save=False)

        elif uploaded_new_image and old_image and new_image and old_image != new_image:
            self._old_image.delete(save=False)

        return instance