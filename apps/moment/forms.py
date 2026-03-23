from django import forms

from apps.moment.models import Moment


class MomentForm(forms.ModelForm):
    """Форма для модели Момент"""
    class Meta:
        model = Moment
        fields = ("title", "details", "image", "music_url", "is_public")

    def clean(self):
        """Общая проверка на то, что должно быть заполнено хотя бы одно из полей"""
        cleaned_data = super().clean()

        details = cleaned_data.get("details")
        image = cleaned_data.get("image")
        music_url = cleaned_data.get("music_url")

        if not details and not image and not music_url:
            raise forms.ValidationError(
                "Момент не может быть пустым (заполните одно из: описание/изображение/музыка."
            )
        return cleaned_data