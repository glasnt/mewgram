from pathlib import Path
import os
import io
import sys
import environ
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Two modes: local dev, and prod.
# Local dev: have a .env file, use local settings.
# Prod: Google auth, use stored settings.
#
# You can interact with prod on your local machine by being
# authenticated to gcloud and not having a local .env file.

env_file = os.path.join(BASE_DIR, ".env")
env = environ.Env()

if os.path.isfile('.env'):
    env.read_env(env_file)
    logging.debug("Loaded env from local filesystem")
    LOCAL_DEVELOPMENT=True

else:
    import google.auth
    try:
        _, project = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError as e:
        raise ImproperlyConfigured("If you want to run in local development mode, define a .env file")

    # Load settings from Secret Manager
    from google.cloud import secretmanager as sm
    client = sm.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
    logging.debug("Loaded env from Secret Manager")
    LOCAL_DEVELOPMENT=False


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

if LOCAL_DEVELOPMENT:
    if "DATABASE_URL" in os.environ.keys():
        DATABASES = { 'default': env.db() }
    else:
        raise ImproperlyConfigured("DATABASE_URL is not defined in .env")
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

STATICFILES_DIRS = ['purr/static']
STATIC_URL = '/static/'

if LOCAL_DEVELOPMENT:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATIC_URL = STATIC_ROOT

    MEDIA_ROOT = "media/"  # where files are stored on the local filesystem
    MEDIA_URL = "/media/"  # what is prepended to the image URL

else:
    GS_BUCKET_NAME = env("GS_BUCKET_NAME", default=None)
    if GS_BUCKET_NAME:
        DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        GS_DEFAULT_ACL = "publicRead"

        INSTALLED_APPS += ["storages"]
    else:
        logging.error("No GS_BUCKET_NAME defined in settings")
        sys.exit(1)
