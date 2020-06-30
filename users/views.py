from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from robohash import Robohash
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout
import io


def user_list(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, "users.html", {"users": users})


def user_detail(request, user_id):
    user = get_user_model().objects.get(email=user_id)
    return render(request, "user_detail.html", {"user": user})


# Implements glasnt/robocat inline
def user_avatar(request, user_id):
    rh = Robohash(user_id)
    rh.assemble(roboset="set4", bgset="bg2")  # 🐱
    avatar = io.BytesIO()
    rh.img.save(avatar, format="PNG")
    avatar.seek(0)
    return HttpResponse(avatar, content_type="image/png")


def settings(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Settings saved.")
    else:
        form = SettingsForm(instance=user)

    return render(request, "settings.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged out. See you again!')
    return HttpResponseRedirect('/')
