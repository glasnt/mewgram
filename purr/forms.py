from django.forms import ModelForm, Textarea
from .models import Purr
from django.contrib.auth import get_user_model

class PurrForm(ModelForm):
    class Meta:
        model = Purr
        fields = ["content"]
        labels = { 'content': "" }
        widgets = {
          'content': Textarea(attrs={'cols': 80, 'rows': 3})
        }

