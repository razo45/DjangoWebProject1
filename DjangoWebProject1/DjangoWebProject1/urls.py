"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


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
    path("create-ticket/", views.create_ticket, name="create_ticket"),
    path("send_mess/", views.send_mess, name="send_mess"),
    path('get_components/', views.get_components, name='get_components'),
    path('api/services/', views.get_services, name='get_services'),
    path('set-theme/', views.set_theme, name='set_theme'),
    path('get_KE/', views.get_KE, name='get_KE'),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('get_usermanual/<int:pk>/', views.get_usermanual, name='get_usermanual'),


    # ADFS
    path('oauth2/', include('django_auth_adfs.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)