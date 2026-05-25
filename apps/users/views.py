from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import User


class RegisterView(CreateView):
    """Контролер регистрации нового пользователя"""
    form_class = CustomUserCreationForm
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("moment:home")


class UserDetailView(LoginRequiredMixin, DetailView):
    """Контролер просмотра профиля пользователя"""
    model = User
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    form_class = CustomUserChangeForm
    template_name = "users/update.html"

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление профиля пользователя"""
    model = User
    template_name = "users/confirm_delete.html"
    success_url = reverse_lazy("moment:home")

    def get_object(self, queryset=None):
        return self.request.user
