from django.shortcuts import render

from .models import Purr

def home(request):
    purrs = Purr.objects.filter(in_reply_to=None).order_by('-date_posted')
    return render(request, 'home.html', {"purrs": purrs})
