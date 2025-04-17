# admin.py
from django.contrib import admin
from .models import CustomUser  # Импортируем вашу модель
  # Импортируем вашу модель

# Регистрируем модель в админке
admin.site.register(CustomUser)
