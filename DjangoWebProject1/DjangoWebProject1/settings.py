"""
Django settings for DjangoWebProject1 project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import posixpath
import ldap
from django_auth_ldap.config import LDAPSearch



AUTH_LDAP_SERVER_URI = "ldap://10.201.42.10"  # ← замените на адрес вашего AD-сервера

AUTH_LDAP_BIND_DN = "nrs"  # ← если нужно логиниться от имени сервиса
AUTH_LDAP_BIND_PASSWORD = "Razo159753852!"

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "OU=SolarSecurity,OU=Domain Users,DC=solar,DC=local",  # ← замените на ваш путь в AD
    ldap.SCOPE_SUBTREE,
    "(sAMAccountName=%(user)s)"  # ищем по логину
)
AUTH_LDAP_CREATE_USERS = True  # создаёт пользователя в Django, если авторизация успешна
AUTH_LDAP_ALWAYS_UPDATE_USER = True

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_LDAP_USER_DN_TEMPLATE = "%(user)s@solar.local"
AUTH_USER_MODEL = 'app.CustomUser'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGIN_URL = "/login/"  # Куда редиректить неавторизованных пользователей
LOGIN_REDIRECT_URL = '/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '186e9c5f-0d7f-4e06-9c32-d26d5d1fe87c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'app',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_auth_adfs',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoWebProject1.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoWebProject1.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]




AUTH_ADFS = {
    "SERVER": "adfs.rt-solar.ru",
    "CLIENT_ID": "your-client-id",
    "RELYING_PARTY_ID": "your-relying-party-id",
    "AUDIENCE": "microsoft:identityserver:your-relying-party-id",
    "CA_BUNDLE": "C:\\Users\\r.nersesyan\\source\repos\\DjangoWebProject1\\DjangoWebProject1\\app\\static\\app\\RT-Solar.Token-Signing.2027.crt.cer",
    "CLAIM_MAPPING": {
        "first_name": "given_name",
        "last_name": "family_name",
        "email": "email",
    },
    "GROUP_CLAIM": "group",
    "MIRROR_GROUPS": True,
    "GROUP_TO_FLAG_MAPPING": {
        "is_staff": ["Django Staff", "Other Django Staff"],
        "is_superuser": "Django Admins",
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))
