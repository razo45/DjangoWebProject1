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
import requests
import json
import pyodbc


from requests.auth import HTTPBasicAuth


@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    username = request.user.username  # Получаем логин пользователя

    default_avatar = static('app/image/NoAvatar.jpg')
    a = get_incidents_list(request.user.initiator_uuid)








    return render(
        request,
        'app/index.html',
        {
            'message': '',
            "username": username,
            "avatar": "",
            'default_avatar': default_avatar,
            'incidents': a,
        }
        

    )




def get_incidents_list(response):
    url = "http://m9-intalev-1c/ITIL/hs/externalapi/getIncidentsList"
    
    # JSON-данные, которые ожидает API
    payload = {
            "startFrom": "0",        
            "initiatorUuid": response       
    }

    # Учетные данные (замени на свои)
    username = "r.nersesyan"
    password = "1234"

    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(username, password),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
            f = json.loads(response.text)
            array = list(f.values())
            array1 = array[0]
            return array1
    else:
        return {"error": f"Ошибка {response.status_code}", "details": response.text}

def get_initiator_uuid(data):
    try:
        # Преобразуем строку JSON в словарь
        parsed_data = json.loads(data)
        
        # Проверяем, что ключ "Initiators" существует и не пуст
        if "Initiators" in parsed_data and parsed_data["Initiators"]:
            # Извлекаем InitiatorUuid первого элемента
            initiator_uuid = parsed_data["Initiators"][0].get("InitiatorUuid")
            return initiator_uuid
        else:
            return None  # Если в "Initiators" нет данных
    except json.JSONDecodeError:
        return None  # Если ошибка в формате JSON

def getInitiators1(request):
    url = "http://m9-intalev-1c/ITIL/hs/externalapi/getInitiators1"
    
    # JSON-данные, которые ожидает API
    payload = {
        "initClientUuid": request
        }

    # Учетные данные (замени на свои)
    username = "r.nersesyan"
    password = "1234"

    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(username, password),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        return response.text
    else:
        return {"error": f"Ошибка {response.status_code}", "details": response.text}




@login_required
def Open_Ticket(request):
    return render(request, 'app/Open_Ticket.html')


@login_required
def logout_view(request):
    logout(request)# Выход из аккаунта
    return redirect("login_view")  # Перенаправление на страницу входа


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")  # Перенаправляем авторизованного пользователя на главную страницу

    if request.method == "POST":
        username = request.POST.get("username")  # Получаем логин
        password = request.POST.get("password")  # Получаем пароль

        user = authenticate(request, username=username, password=password)  # Проверяем пользователя

        if user is not None:  # Если логин/пароль верные

            uuid = get_initiator_uuid(getInitiators1(username))
            user.initiator_uuid = uuid
            user.save()

            login(request, user)



            return redirect("home") # Перенаправляем на главную страницу
        else:
            return render(request, 'app/login.html', {"error": "Неверный логин или пароль"})  # Ошибка

    return render(request, 'app/login.html')  # Если `GET`, просто показываем форму



