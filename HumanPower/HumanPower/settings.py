#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django settings for PlayMate project.

Generated by 'django-admin startproject' using Django 1.8.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ma014-od5mvq59ew!h1=4c1#((av$5)tlsv$o9(&q4^(h)0t-2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
   
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'human',

    'widget_tweaks',
    'mapwidgets',
    'crispy_forms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'HumanPower.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'HumanPower.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'human', # Database 名
        'USER': 'postgres', # postgre 使用者帳號
        'PASSWORD': 'ps60818', # postgre 使用者密碼
        'HOST': 'localhost', # postgre 架設的 server 位置，預設是本機
        'PORT': '', # postgre 架設的 post，設定 '' 使用預設
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh_Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

#AUTH_USER_MODEL = 'main.User'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,  'static'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# GOOGLE MAP 設定
GOOGLE_MAPS_API_KEY = 'AIzaSyCK7EpwIg_1SOaFDLNEWTFAJSDf0ltI-N0'

MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 10),
        ("mapCenterLocation", [25.046257533006948, 121.51756463976403]),
    ),
    "GOOGLE_MAP_API_KEY": "AIzaSyCK7EpwIg_1SOaFDLNEWTFAJSDf0ltI-N0",
    "LANGUAGE": 'zh_Hant',
}

# OSGeo4W 設定
if os.name == 'nt':
    import platform
    OSGEO4W = r"C:\OSGeo4W" # 設定 osgeo4w 安裝路徑
    if '64' in platform.architecture()[0]:
        OSGEO4W += "64"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
