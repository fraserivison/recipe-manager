"""
Django settings for the Sizzle project.

This module contains all the configuration settings for the Sizzle project.
It includes settings for database connections, third-party services like
Cloudinary, security settings, and app configurations.

Make sure to keep sensitive information such as the secret key and database
credentials secure by using environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Cloudinary configuration
cloudinary.config(
    cloudinary_url=CLOUDINARY_URL
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

CSRF_TRUSTED_ORIGINS = [
    'https://*.gitpod.io',
    'https://sizzle-recipe-manager.herokuapp.com',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'crispy_forms',
    'django_summernote',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'recipes',
]

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap5'

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = True
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sizzle.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), BASE_DIR],
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

WSGI_APPLICATION = 'sizzle.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

CSRF_TRUSTED_ORIGINS = [
    "https://*.codeinstitute-ide.net/",
    "https://sizzle-recipe-manager.herokuapp.com",
    "https://8000-fraserivison-sizzle-0yosmcb7l6q.ws-eu116.gitpod.io",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
