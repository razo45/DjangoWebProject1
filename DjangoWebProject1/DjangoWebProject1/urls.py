"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/',views.login_view, name='login_view'),
    path('Whoops/',views.Whoops, name='Whoops'),
    path("logout/", views.logout_view, name="logout"),
    path("Open_Ticket/<str:ticket_uuid>", views.Open_Ticket, name="Open_Ticket"),
    path("Download_File/<str:file_uuid>", views.Download_File, name="Download_File"),
    path("filter-incidents/", views.filter_incidents, name="filter_incidents"),
    path("Search_Ticket/", views.Open_Ticket_Search, name="Open_Ticket_Search"),

    # ADFS
    path('oauth2/', include('django_auth_adfs.urls')),
]
