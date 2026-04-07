from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.urls import path, reverse_lazy

from apps.users.forms import CustomAuthenticationForm, CustomPasswordChangeForm
from apps.users.views import (
    RegisterView,
    UserDeleteView,
    UserDetailView,
    UserUpdateView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="profile"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="confirm_delete"),
    path(
        "password-change/",
        PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=CustomPasswordChangeForm,
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done",
    ),
]
