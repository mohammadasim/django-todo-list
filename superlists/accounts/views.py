import uuid
import sys

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from accounts.models import Token, ListUser


def send_login_email(request):
    email = request.POST.get('email')
    if ListUser.objects.filter(email=email).exists():
        pass
    else:
        ListUser.objects.create(email=email)
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('Save uid ', uid, 'for email ', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in:\n\n{url}',
        'noreply@superlists.com',
        [email],
    )
    return render(request, 'accounts/login_email_sent.html')


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')
