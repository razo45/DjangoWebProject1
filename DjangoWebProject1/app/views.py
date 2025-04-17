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
from requests.auth import HTTPBasicAuth
import requests
import json
import pyodbc
import html
import re
from bs4 import BeautifulSoup
# === Блок динамического обновления страниц === ↓

@login_required
def filter_incidents(request): # Динамическое обновение списка обращений пользователя
    state = request.GET.get("state", "all")
    all_incidents = list(get_incidents_list(request.user.initiator_uuid))

    if state == "Всего":
        filtered = all_incidents
    elif state == "Открыто":
        filtered = [i for i in all_incidents if i.get("state") != 'Закрыто']
    else:
        filtered = [i for i in all_incidents if i.get("state") == 'Закрыто']

    return render(request, "app/partials/incidents_list.html", {"incidents": filtered})


def clean_html(text):
    decoded = html.unescape(text)
    soup = BeautifulSoup(decoded, "html.parser")

    def is_visually_empty(tag):
        if tag.find(["img", "iframe"]):
            return False
        clean_text = re.sub(r'[\s\u00a0]+', '', tag.get_text())
        return not clean_text

    # Удаляем только реально пустые
    for tag in soup.find_all(["p", "span", "div"]):
        if is_visually_empty(tag):
            tag.decompose()

    return str(soup)




# === Блок Взаимодействия с API и обработка данныз === ↓

def get_incidents_list(initiator_uuid):  # <-- Переименовали параметр
    url = "http://m9-intalev-1c/ITIL/hs/externalapi/getIncidentsList"
    
    payload = {
        "startFrom": "0",        
        "initiatorUuid": initiator_uuid  # <-- используем новый параметр
    }

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
        return list(f.values())[0]
    else:
        return {"error": f"Ошибка {response.status_code}", "details": response.text}

def get_initiator_uuid(data): # Получение UUID пользователя из getInitiators1 
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
        return None 

def getInitiators1(request): # Получение информации о пользователе через его логин 
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

def extGetDetailIncidentInfo(request): # Получение информации о пользователе через его логин 
    url = "http://m9-intalev-1c/ITIL/hs/externalapi/extGetDetailIncidentInfo"
    
    # JSON-данные, которые ожидает API
    payload = {
        "Uuid": request
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
        array = f
        return array
    else:
        return {"error": f"Ошибка {response.status_code}", "details": response.text}

# === Блок открытия страниц === ↓

@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    initiator_uuid = request.user.initiator_uuid
    default_avatar = static('app/image/NoAvatar.jpg')
    incidents =list(get_incidents_list(initiator_uuid))
    count_closed = sum(1 for incident in incidents if incident.get("state") == 'Закрыто')
    count_open = sum(1 for incident in incidents if incident.get("state") != 'Закрыто')
    count_all = len(incidents)


    return render(
        request,
        'app/index.html',
        {
            'message': '',
            "user": request.user,
            "avatar": "",
            'default_avatar': default_avatar,
            'incidents': incidents,
            'count_closed': count_closed,
            'count_open': count_open,
            'count_all': count_all,
        }
        

    ) # Страница всех тикетов пользователя

@login_required
def Open_Ticket_Search(request):
    if request.user.is_seach:
        num = request.GET.get("uuid")
        if num:


            url = "http://m9-intalev-1c/ITIL/hs/externalapi/getIncidentsList"
    
            payload = {
                "startFrom": "0",        
                "number": num  # <-- используем новый параметр
            }

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
                incidents =list(list(f.values())[0])
                if len(incidents) > 0:
                    uuid = incidents[0]["linkUuid"]
                    return redirect("Open_Ticket", ticket_uuid=uuid)
                else:
                    return redirect("Whoops")
            else:
                return redirect("Whoops")
    return redirect("home")

@login_required
def Whoops(request):

    return render(request, 'app/Whoops.html')  # Если `GET`, просто показываем форму




@login_required
def Open_Ticket(request, ticket_uuid):
    all_incidents = extGetDetailIncidentInfo(ticket_uuid)
    # Раскодируем HTML в каждом сообщении
    for msg in all_incidents.get("TheHistoryOfCommunication", []):
        msg["html_render"] = clean_html(msg.get("HTMLText", ""))
    return render(
        request, 
        'app/Open_Ticket.html',
        {
            'message': '',
            "user": request.user,
            'incident_info': all_incidents,

        }
) # Страница подробной информации о тикете



@login_required
def logout_view(request):
    logout(request)# Выход из аккаунта
    return redirect("login_view")  # Выход из профиля

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