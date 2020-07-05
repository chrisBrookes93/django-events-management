from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name='user_register'),
    path('login', LoginView.as_view(template_name='users/login.html'), name='user_login'),
    path('logout', LogoutView.as_view(), name='user_logout'),
]
