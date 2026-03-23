from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.users.views import RegisterView, UserDetailView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile'),
]