from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from hashid_field import HashidField
from django.contrib.humanize.templatetags.humanize import naturaltime


class Purr(models.Model):
    id = HashidField(primary_key=True, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=140)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)
    in_reply_to = models.ForeignKey("self", default=None, blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def relative_date(self):
        return naturaltime(self.date_posted)

    @property
    def display_name(self):
        return self.user.display_name or self.user.email

    @property
    def can_reply(self):
        return self.in_reply_to is None

    def replies(self):
        return Purr.objects.filter(in_reply_to=self.id).order_by('-date_posted')

    def __repr__(self):
        return f"{self.user}: {self.content} ({self.relative_date})"

    def __str__(self):
        return repr(self)

