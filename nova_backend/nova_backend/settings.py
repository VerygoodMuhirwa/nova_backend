"""
Django settings for nova_backend project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'm6tk7jj_49s9m89y0h57zlsmy7_kvh$(y@2d(x%k3%b-3s=^t^'
CSRF_COOKIE_SECURE = True
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "194.163.167.131",
    "localhost"
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'drf_yasg',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'user.apps.UserConfig',
    'verification.apps.VerificationConfig',
    'sensorapp.apps.SensorappConfig',
    'channels',
]


# ASGI_APPLICATION = 'nova_backend.settings'
WSGI_APPLICATION = 'nova_backend.wsgi.application'
ASGI_APPLICATION = 'nova_backend.asgi.application'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587  # Use port 587 for TLS encryption, or update to your SMTP server's appropriate port
EMAIL_HOST_USER = 'verygoodmuhirwa2@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'stqm hzai agfy adjz'  # Use the generated app password here
DEFAULT_FROM_EMAIL = 'verygoodmuhirwa2@gmail.com' 
EMAIL_APP_NAME = 'Django SMTP'  # This is the custom name you provided during app password generation

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        }
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


AUTHENTICATION_BACKENDS = [
                           'django.contrib.auth.backends.ModelBackend', ]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nova_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # 'default': {
    #     'ENGINE': 'djongo',
    #     'ENFORCE_SCHEMA': False,
    #     'NAME': 'nova_project',
    #     'CLIENT': {
    #         'host': 'localhost',
    #         'port': 27017,
    #     }
    # },
    'mongodb_atlas': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'NAME': 'nova_project',

        'CLIENT': {
            'host': 'cluster0.c5iqqff.mongodb.net',
            'username': 'VerygoodMuhirwa',  
            'password': 'Verygood',  
            'authSource': 'admin',  
            'authMechanism': 'SCRAM-SHA-1', 
        }
    }
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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

CORS_ALLOWED_ORIGINS = [
    "https://nova-ruddy.vercel.app",
    "http://localhost:3000",
    "http://194.163.167.131",
    "http://localhost:8081",
    "exp://10.5.222.221:8081"
]

# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['Authorization', 'Content-Type', 'Cookie']


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

