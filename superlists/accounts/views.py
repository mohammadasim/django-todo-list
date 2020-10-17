from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    mesage_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        mesage_body,
        'noreply@superlists',
        [email]
    )
    messages.success(request,
                     "Check your email, we've sent you a link you can use to log in.")
    return redirect("/")


def login(request):
    return redirect("/")
