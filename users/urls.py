from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('users', views.user_list, name="user_list"),
    path('users/<user_id>', views.user_detail, name="user_detail"),
    path('users/<user_id>/avatar', views.user_avatar, name="user_avatar"),
    path('settings', views.settings, name="settings"),
]
