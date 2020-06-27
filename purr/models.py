from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Purr(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    date_posted = models.DateTimeField(default=timezone.now)
    in_reply_to = models.ForeignKey("self", default=None, null=True, on_delete=models.SET_NULL)

    def replies(self):
        return Purr.objects.filter(in_reply_to=self.id).order_by('date_posted')
