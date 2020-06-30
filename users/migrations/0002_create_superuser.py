import os
from django.contrib.auth import get_user_model

from django.db import migrations

import google.auth
from google.cloud import secretmanager_v1beta1 as sm
_, project = google.auth.default()

def access_secret(secret_key):
    if project and not os.path.isfile('.env'):
        client = sm.SecretManagerServiceClient()
        path = client.secret_version_path(project, secret_key, "latest")
        payload = client.access_secret_version(path).payload.data.decode("UTF-8")
        return payload
    else:
        return os.environ[secret_key]

def createsuperuser(apps, schema_editor):
    email = access_secret("ADMINEMAIL")
    password = access_secret("ADMINPASS")

    # Create a new user using acquired password
    User = get_user_model()
    User.objects.create_superuser(email, password=password)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [migrations.RunPython(createsuperuser)]
