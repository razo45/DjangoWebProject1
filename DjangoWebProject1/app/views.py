"""
Definition of views.
"""
# -*- coding: utf-8 -*-

from datetime import datetime
from email import message
from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.templatetags.static import static

@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    username = request.user.username  # Получаем логин пользователя
    default_avatar = static('app/image/NoAvatar.jpg')
    return render(
        request,
        'app/index.html',
        {
            'message': '',
            "username": username,
            "avatar": "",
            'default_avatar': default_avatar,
        }
    )


def logout_view(request):
    logout(request)# Выход из аккаунта
    return redirect("login_view")  # Перенаправление на страницу входа

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Получаем логин
        password = request.POST.get("password")  # Получаем пароль

        user = authenticate(request, username=username, password=password)  # Проверяем пользователя

        if user is not None:  # Если логин/пароль верные
            login(request, user)
            return render(request, 'app/login.html', {"error": "Верный логин и пароль"})  # Ошибка  # Перенаправляем на главную страницу
        else:
            return render(request, 'app/login.html', {"error": "Неверный логин или пароль"})  # Ошибка

    return render(request, 'app/login.html')  # Если `GET`, просто показываем форму



