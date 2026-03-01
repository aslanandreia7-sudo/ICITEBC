"""
Django settings for core project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- CONFIGURACIÓN DE SEGURIDAD ---

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z*8n4vxvpi4y+cdsx@rq@r9hm+t*f=zvy!n+w-^i%_imtr$vrf'

# SECURITY WARNING: don't run with debug turned on in production!
# CAMBIADO A TRUE PARA DESARROLLO LOCAL
DEBUG = True

# AGREGADOS 127.0.0.1 Y LOCALHOST PARA QUE NO DE ERROR 400 EN TU PC
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'icitebc.lat', 'www.icitebc.lat', '.onrender.com']


# --- DEFINICIÓN DE APLICACIONES ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plataforma',  # Tu aplicación principal
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir archivos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Directorio global de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# --- BASE DE DATOS ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- VALIDACIÓN DE CONTRASEÑAS ---

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]


# --- INTERNACIONALIZACIÓN ---

LANGUAGE_CODE = 'es-mx' # Cambiado a español de México

TIME_ZONE = 'America/Tijuana' # Ajustado a tu zona horaria

USE_I18N = True

USE_TZ = True


# --- ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES) ---

STATIC_URL = '/static/'

# Donde se guardan tus archivos de diseño originales
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Carpeta donde Django junta todo para producción (Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de WhiteNoise para que no falle si falta algún archivo
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'