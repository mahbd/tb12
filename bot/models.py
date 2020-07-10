from django.db import models


class BotAccessInfo(models.Model):
    type = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    chat_id = models.TextField(blank=True, null=True)
    last_date = models.DateTimeField(blank=True, null=True)
    first_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
