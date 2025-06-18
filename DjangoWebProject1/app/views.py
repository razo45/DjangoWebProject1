"""
Definition of views.
"""
# -*- coding: utf-8 -*-

import code
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
import base64
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GlobalSettings

# === Блок динамического обновления страниц === ↓
settings = GlobalSettings.get_solo()
# settings.URL_ITILIUM = "http://m9-intalev-1c/ITIL/hs/externalapi/"
# settings.usernameAPI = "r.nersesyan"
# settings.passwordAPI = "1234"

@login_required
def filter_incidents(request): # Динамическое обновение списка обращений пользователя
    state = request.GET.get("state", "all")
    all_incidents = list(get_incidents_list(request.user.initiator_uuid))

    if state == "Всего":
        filtered = all_incidents
    elif state == "Открыто":
        filtered = [i for i in all_incidents if i.get("state") != 'Закрыто' and i.get("state") != 'Отклонено']
    else:
        filtered = [i for i in all_incidents if i.get("state") == 'Закрыто' or i.get("state") == 'Отклонено']

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

# === Блок Взаимодействия с API и обработка данных === ↓

def get_incidents_list(initiator_uuid):  # <-- Переименовали параметр
    url = settings.URL_ITILIUM + "getIncidentsList"
    
    payload = {
        "startFrom": "0",        
        "initiatorUuid": initiator_uuid  # <-- используем новый параметр
    }




    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
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

def get_initiator_code(data): # Получение UUID пользователя из getInitiators1 
    try:
        # Преобразуем строку JSON в словарь
        parsed_data = json.loads(data)
        
        # Проверяем, что ключ "Initiators" существует и не пуст
        if "Initiators" in parsed_data and parsed_data["Initiators"]:
            # Извлекаем InitiatorUuid первого элемента
            initiator_uuid = parsed_data["Initiators"][0].get("InitiatorCode")
            return initiator_uuid
        else:
            return None  # Если в "Initiators" нет данных
    except json.JSONDecodeError:
        return None 

def get_Client_uuid(data): # Получение UUID пользователя из getInitiators1 
    try:
        # Преобразуем строку JSON в словарь
        parsed_data = json.loads(data)
        
        # Проверяем, что ключ "Initiators" существует и не пуст
        if "Initiators" in parsed_data and parsed_data["Initiators"]:
            # Извлекаем InitiatorUuid первого элемента
            initiator_uuid = parsed_data["Initiators"][0].get("InitiatorOwner")
            return initiator_uuid
        else:
            return None  # Если в "Initiators" нет данных
    except json.JSONDecodeError:
        return None 

def getInitiators1(request): # Получение информации о пользователе через его логин 
    url = settings.URL_ITILIUM + "getInitiators1"
    
    # JSON-данные, которые ожидает API
    payload = {
        "initClientUuid": request
        }

    # Учетные данные (замени на свои)



    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        return response.text
    else:
        return {"error": f"Ошибка {response.status_code}", "details": response.text}

def extGetDetailIncidentInfo(request): # Получение информации о пользователе через его логин 
    url = settings.URL_ITILIUM + "extGetDetailIncidentInfo"
    
    # JSON-данные, которые ожидает API
    payload = {
        "Uuid": request
        }

    # Учетные данные (замени на свои)



    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        f = json.loads(response.text)
        array = f
        return array
    else:
        return {"error": f"Ошибка {response.status_code}", "details": response.text}
        return {"error": f"Ошибка {response.status_code}", "details": response.text}

def extGetFileData(request): # Получение файло по uuid 
    url = settings.URL_ITILIUM + "extGetFileData"
    
    # JSON-данные, которые ожидает API
    payload = {
        "idFile": request
        }

    # Учетные данные (замени на свои)



    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        f = json.loads(response.text)
        array = f
        return array
    else:
        return {"error": f"Ошибка {response.status_code}", "details": response.text}
        return {"error": f"Ошибка {response.status_code}", "details": response.text}

def get_services(request):
    url = settings.URL_ITILIUM + "getServices"
    payload = {}
        # Учетные данные (замени на свои)



    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        raw = response.json()
        components = [
            {
                "uuid": item["ServiceUuid"],
                "name": item["Service"]
            }
            for item in raw.get("Services", [])
        ]
        return JsonResponse({"services": components})
    return JsonResponse({"services": []})

def get_components(request):
    uuid = request.GET.get('uuid')
    if not uuid:
        return JsonResponse({'components': []})

    url = settings.URL_ITILIUM + "getServiceComponents"
    payload = {
        "servCompServiceUuid": uuid
        }
        # Учетные данные (замени на свои)



    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        raw = response.json()
        components = [
            {
                "uuid": item["ServiceComponentUuid"],
                "name": item["ServiceComponent"]
            }
            for item in raw.get("ServiceComponents", [])
        ]
        return JsonResponse({"components": components})
    return JsonResponse({"components": []})

def get_KE(request):
    code = request.user.initiator_code
    if not code:
        return JsonResponse({'components': []})

    url = settings.URL_ITILIUM + "getInitiatorsKE"
    payload = {
        "initClientCode": code
        }
        # Учетные данные (замени на свои)



    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        raw = response.json()
        components = [
            {
                "NAME": item["InitiatorKE"],
                "INV": item["InitiatorKeInvN"],
                "LOC": item["InitiatorKeLocation"],
                "CLASS": item["InitiatorKeClassification"]
            }
            for item in raw.get("Initiators", [])
        ]
        return JsonResponse({"components": components})
    return JsonResponse({"components": []})


@require_http_methods(["GET", "POST"])
def create_ticket(request):
    if request.method == "POST":
        title = request.POST.get("title")
        service = request.POST.get("service")
        component = request.POST.get("component")
        typeuuid = request.POST.get("type")
        comment = request.POST.get("comment")
        files = request.FILES.getlist("attachments")  # <--- Получаем список файлов


        files_payload = []

        for f in files:
            # Чтение и кодирование в base64
            file_data = f.read()
            encoded_data = base64.b64encode(file_data).decode("utf-8")

            files_payload.append({
                "Name": f.name,
                "Data": encoded_data
            })

        url = settings.URL_ITILIUM + "performCustomActionWithIncident"
    
        payload = {
            "Action" : "RegisterIncident",
            "ClientUuid" : request.user.Client_uuid,
            "InitiatorUuid" : request.user.initiator_uuid,
            "ServiceUuid" : service,
            "CompositionServiceUuid" : component,
            "TypeUuid" : typeuuid,
            "Topic" : title,
            "Description" : comment,
            "Files" : files_payload

        }


    
    

        response = requests.post(
            url,
            json=payload,
            auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return redirect("home")  # или куда нужно
        else:
            return redirect("home")

def send_mess(request):
    if request.method == "POST":
        Mess = request.POST.get("Message")
        uuid = request.POST.get("uuid")
        files = request.FILES.getlist("file")  # <--- Получаем список файлов


        files_payload = []

        for f in files:
            # Чтение и кодирование в base64
            file_data = f.read()
            encoded_data = base64.b64encode(file_data).decode("utf-8")

            files_payload.append({
                "Name": f.name,
                "Data": encoded_data
            })

        url = settings.URL_ITILIUM + "performCustomActionWithIncident"
    
        payload = {
            "Action" : "AddNewCommunicationWithFile",
            "IncUuid" : uuid,
            "Commentary" : Mess,
            "Files" : files_payload

        }


    
    

        response = requests.post(
            url,
            json=payload,
            auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return redirect("Open_Ticket", ticket_uuid=uuid)  
        else:
            return redirect("Open_Ticket", ticket_uuid=uuid)




            





# === Блок открытия страниц === ↓

@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    initiator_uuid = request.user.initiator_uuid
    default_avatar = static('app/image/NoAvatar.jpg')
    incidents =list(get_incidents_list(initiator_uuid))
    count_closed = sum(1 for incident in incidents if incident.get("state") == 'Закрыто' or incident.get("state") == 'Отклонено')
    count_open = sum(1 for incident in incidents if incident.get("state") != 'Закрыто' and incident.get("state") != 'Отклонено')
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


            url = settings.URL_ITILIUM + "getIncidentsList"
    
            payload = {
                "startFrom": "0",        
                "number": num  # <-- используем новый параметр
            }

        
        

            response = requests.post(
                url,
                json=payload,
                auth=HTTPBasicAuth(settings.usernameAPI, settings.passwordAPI),
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
def Download_File(request, file_uuid):
    file = extGetFileData(file_uuid)
    file_data = base64.b64decode(file['Data'])
    response = HttpResponse(file_data, content_type='application/octet-stream')
    name = file['Name']
    response['Content-Disposition'] = f'attachment; filename="{name}"'
    return response

@login_required
def Open_Ticket(request, ticket_uuid):
    all_incidents = extGetDetailIncidentInfo(ticket_uuid)
    all_files = all_incidents.get("FilesDefinitions",[])
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
            'all_files': all_files,

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
            data = getInitiators1(username)
            user.initiator_uuid = get_initiator_uuid(data)
            user.Client_uuid = get_Client_uuid(data)
            user.initiator_code = get_initiator_code(data)
            user.save()

            login(request, user)

            return redirect("home") # Перенаправляем на главную страницу
        else:
            return render(request, 'app/login.html', {"error": "Неверный логин или пароль"})  # Ошибка

    return render(request, 'app/login.html')  # Если `GET`, просто показываем форму

@csrf_exempt  # если используешь @login_required, не забудь добавить @csrf_exempt после него
def set_theme(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        theme = data.get('theme')
        if theme in ['dark', 'light']:
            request.user.preferredTheme = theme
            request.user.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)