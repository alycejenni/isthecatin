import dj_database_url
import os
from .env import *

ALLOWED_HOSTS = ['isthecatin.herokuapp.com', 'www.isthecat.in', 'isthecat.in']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'controlcenter'
    ]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ]

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
LOGIN_REDIRECT_URL = '/'
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                ],
            },
        },
    ]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(engine='django.db.backends.postgresql_psycopg2')
    }

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

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.join(BASE_DIR, 'app')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# DASHBOARDS
CONTROLCENTER_DASHBOARDS = ()
