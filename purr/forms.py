from django.forms import ModelForm
from .models import Purr


class PurrForm(ModelForm):
    class Meta:
        model = Purr
        fields = ["content"]
        labels = { 'content': "" }

