from django.contrib.auth.views import LoginView
from django.urls import path
from .views import signup_view, logout_view

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='account_login'),
    path('signup/', signup_view, name='account_signup'),
    path('logout/', logout_view, name='account_logout'),
]