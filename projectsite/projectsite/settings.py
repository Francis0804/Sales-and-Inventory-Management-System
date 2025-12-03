from pathlib import Path
import os
import socket

# ---------------- BASE DIR ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- SECURITY ----------------
SECRET_KEY = 'django-insecure-replace-this-with-your-secret-key'
DEBUG = True

# ---------------- ALLOWED HOSTS ----------------
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'sales-and-inventory-system.pythonanywhere.com']

# ---------------- INSTALLED APPS ----------------
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Third-party
    'widget_tweaks',

    # Local apps
    'core',
]

# ---------------- SITE ID ----------------
# SITE_ID = 1 for local, 2 for PythonAnywhere
SITE_ID = 2 if "pythonanywhere" in socket.gethostname() else 1

# ---------------- AUTHENTICATION ----------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

# ---------------- URLS / WSGI ----------------
ROOT_URLCONF = 'projectsite.urls'
WSGI_APPLICATION = 'projectsite.wsgi.application'

# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------- DATABASE ----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- PASSWORD VALIDATORS ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- LANGUAGE & TIMEZONE ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC FILES ----------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------- MEDIA FILES ----------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------- DEFAULT PRIMARY KEY ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Where to redirect users after login
LOGIN_REDIRECT_URL = '/'
