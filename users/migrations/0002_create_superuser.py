import os
from django.contrib.auth import get_user_model

from django.db import migrations
"""
import google.auth
from google.cloud import secretmanager_v1beta1 as sm
def access_secrets(secret_keys):
    secrets = {}
    _, project = google.auth.default()
    if project:
        client = sm.SecretManagerServiceClient()
        for s in secret_keys:
            path = client.secret_version_path(project, s, "latest")
            payload = client.access_secret_version(path).payload.data.decode("UTF-8")
            secrets[s] = payload
    return secrets
"""
def createsuperuser(apps, schema_editor):
    settings = ["ADMINEMAIL", "ADMINPASS"]
#    if not all (k in os.environ.keys() for k in set(settings)):
#        secrets = access_secrets(settings)
#        email = secrets["ADMINEMAIL"]
#        password = secrets["ADMINPASS"]
    email = os.environ["ADMINEMAIL"]
    password = os.environ["ADMINPASS"]

    # Create a new user using acquired password
    User = get_user_model()
    User.objects.create_superuser(email, password=password)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [migrations.RunPython(createsuperuser)]
