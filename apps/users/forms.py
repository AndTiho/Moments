from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserChangeForm, UserCreationForm)

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации пользователя с не стандартными полями формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update(
            {
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "Придумай пароль для входа...",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "Повтори пароль",
            }
        )

    class Meta:
        model = User
        fields = ("username", "first_name", "email")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full rounded-2xl",
                    "placeholder": "Придумай никнэйм",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full rounded-2xl",
                    "placeholder": "Как тебя можно называть?",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "input input-bordered w-full rounded-2xl",
                    "placeholder": "Куда лететь голубям@почты.com...?",
                }
            ),
        }


class CustomUserChangeForm(UserChangeForm):
    """Форма для редактирования профиля с не стандартными полями формы"""
    password = None

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "about_me",
            "header_name_preference",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full rounded-2xl",
                    "placeholder": "Твой никнэйм",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "input input-bordered w-full rounded-2xl",
                    "placeholder": "Куда лететь голубям@почты.com...?",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full rounded-2xl",
                    "placeholder": "Твоё имя",
                }
            ),
            "about_me": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full rounded-2xl min-h-32",
                    "placeholder": "Пара слов о себе",
                }
            ),
            "header_name_preference": forms.Select(
                attrs={
                    "class": "select select-bordered w-full rounded-2xl",
                }
            ),
        }


class CustomAuthenticationForm(AuthenticationForm):
    """Форма для логина с не стандартными полями формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "Никнэйм",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "Пароль",
            }
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Форма для изменения пароля с не стандартными полями формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].widget.attrs.update(
            {
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "Старый пароль",
            }
        )
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "Новый пароль",
            }
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "input input-bordered w-full rounded-2xl",
                "placeholder": "Подтверждение пароля",
            }
        )
