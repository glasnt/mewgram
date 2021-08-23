import os
from django.contrib.auth import get_user_model

from django.db import migrations
from django.conf import settings




def access_secret(secret_key):
    if settings.LOCAL_DEVELOPMENT:
        return os.environ[secret_key]

    else:
        import google.auth
        from google.cloud import secretmanager as sm
        _, project = google.auth.default()

        client = sm.SecretManagerServiceClient()
        name = client.secret_version_path(project, secret_key, "latest")
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
        return payload

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
