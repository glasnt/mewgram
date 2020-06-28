from django.forms import ModelForm
from .models import Purr
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin

class PurrForm(ModelForm):
    class Meta:
        model = Purr
        fields = ["content"]
        labels = { 'content': "" }

class SettingsForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["display_name"]

