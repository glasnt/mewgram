from django.contrib import admin

from .models import Purr


@admin.register(Purr)
class PurrAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.object_id = object_id
        return super(PurrAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "in_reply_to":
            kwargs['queryset'] = Purr.objects.exclude(pk=self.object_id)
        return super(PurrAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
