from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('reply/<purr_id>', views.reply, name="reply")
]
