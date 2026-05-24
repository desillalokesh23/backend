"""
Django settings for Global TMS backend.
Local configuration is inlined (no .env) per project requirements.
"""

from datetime import timedelta
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Logging directory
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

SECRET_KEY = 'django-insecure-&07+aol5&a2schk_h2#^7dg0&!f@#%lzc0%7ei5im(it4tn+of'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'master',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'master.middleware.tenant_restriction.TenantRestrictionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database — SQLite for local development (file-based, no server required)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MySQL (future production) — uncomment and remove SQLite block above when ready:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'global_tms',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'master.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
CORS_ALLOW_CREDENTIALS = True

SPECTACULAR_SETTINGS = {
    'TITLE': 'Global TMS API',
    'DESCRIPTION': 'Enterprise multi-tenant logistics platform',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'SECURITY': [{'BearerAuth': []}],
    'SECURITY_SCHEMES': {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    },
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
    ],
}

# ==============================================
# LOGGING CONFIGURATION (Production Ready)
# ==============================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{levelname}] [{name}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django.log',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'error.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'security.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'WARNING',
        },
    },
    'loggers': {
        # Django framework logs
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'security_file'],
            'level': 'WARNING',
            'propagate': False,
        },

        # Your main application
        'master': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },

        # Root logger (catch-all)
        '': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
        },
    },
}
