"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login_view, name='login_view'),
    path("logout/", views.logout_view, name="logout"),
    path("Open_Ticket/", views.Open_Ticket, name="Open_Ticket"),


]
