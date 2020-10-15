from django.urls import path

from .views import send_login_email
urlpatterns = [
    path('send_login_email', send_login_email, name='login_email')
]