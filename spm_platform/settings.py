import os
from pathlib import Path

import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent


# Security

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-development-key-change-in-production',
)

DEBUG = os.environ.get(
    'DEBUG',
    'True',
).lower() in {
    'true',
    '1',
    'yes',
}


# Hosts

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)


# CSRF trusted origins

CSRF_TRUSTED_ORIGINS = []

render_external_url = os.environ.get('RENDER_EXTERNAL_URL')

if render_external_url:
    CSRF_TRUSTED_ORIGINS.append(render_external_url)


# Applications

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.accounts',
    'apps.properties',
    'apps.appliances',
    'apps.maintenance',
    'apps.notifications',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'spm_platform.urls'


TEMPLATES = [
    {
        'BACKEND': (
            'django.template.backends.django.DjangoTemplates'
        ),
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                (
                    'django.template.context_processors.request'
                ),
                (
                    'django.contrib.auth.context_processors.auth'
                ),
                (
                    'django.contrib.messages.context_processors.messages'
                ),
            ],
        },
    },
]


WSGI_APPLICATION = 'spm_platform.wsgi.application'


# Database
#
# Local development:
# SQLite is used when DATABASE_URL is not available.
#
# Render:
# PostgreSQL is used through the DATABASE_URL
# environment variable.

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Custom user model

AUTH_USER_MODEL = 'accounts.User'


# Authentication navigation

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_TZ = True


# Static files

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = []


STORAGES = {
    'default': {
        'BACKEND': (
            'django.core.files.storage.FileSystemStorage'
        ),
    },
    
    'staticfiles': {
        'BACKEND': (
            'whitenoise.storage.'
            'CompressedStaticFilesStorage'
        ),
    },
}


# Default primary-key type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Jazzmin administration interface

JAZZMIN_SETTINGS = {
    'site_title': 'SPM Admin',
    'site_header': 'Smart Property Maintenance',
    'site_brand': 'SPM Administration',
    'welcome_sign': (
        'Welcome to Smart Property Maintenance Administration'
    ),
    'copyright': 'Smart Property Maintenance Platform',
    'show_sidebar': True,
    'navigation_expanded': True,
    'show_ui_builder': False,
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}



# Production security

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https',
    )

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = True

    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    X_FRAME_OPTIONS = 'DENY'

    SECURE_CONTENT_TYPE_NOSNIFF = True