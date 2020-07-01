from pathlib import Path
import os
import io
import environ
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

env_file = os.path.join(BASE_DIR, ".env")
env = environ.Env()

import google.auth
_, project = google.auth.default()

if os.path.isfile('.env'):
    env.read_env(env_file)
    logging.debug("Loaded env from local filesystem")
else:
    if project:
        from google.cloud import secretmanager_v1beta1 as sm
        client = sm.SecretManagerServiceClient()
        settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
        path = client.secret_version_path(project, settings_name, "latest")
        payload = client.access_secret_version(path).payload.data.decode("UTF-8")

        env.read_env(io.StringIO(payload))
        logging.debug("Loaded env from Secret Manager")


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", default=False)

LOGIN_REDIRECT_URL = "/"

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'gcloudc',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'users',
    'purr',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mewgram.urls'

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

WSGI_APPLICATION = 'mewgram.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

if "DATABASE_URL" in os.environ.keys():
    DATABASES = { 'default': env.db() }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'gcloudc.db.backends.datastore',
            'PROJECT': project,
            'INDEXES_FILE': "djangaeidx.yaml",
            "NAMESPACE": "mewgram",
        }
    }

logging.debug(f"Using {DATABASES['default']['ENGINE']} as database engine")

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'users.CustomUser'
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


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = ['purr/static']

GS_BUCKET_NAME = env("GS_BUCKET_NAME", default=None)
if GS_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"

    INSTALLED_APPS += ["storages"]
    STATIC_URL = STATIC_ROOT

else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    STATIC_URL = STATIC_ROOT

    MEDIA_ROOT = "media/"  # where files are stored on the local filesystem
    MEDIA_URL = "/media/"  # what is prepended to the image URL
