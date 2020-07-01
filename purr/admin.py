from django.contrib import admin

from .models import Purr



@admin.register(Purr)
class PurrAdmin(admin.ModelAdmin):
    pass
