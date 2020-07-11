from django.db import models


class BotAccessInfo(models.Model):
    type = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    chat_id = models.TextField(blank=True, null=True)
    last_date = models.DateTimeField(blank=True, null=True)
    first_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MemberList(models.Model):
    member_name = models.TextField(blank=True, null=True)
    member_id = models.TextField(blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    group = models.ManyToManyField(BotAccessInfo, blank=True)

    def __str__(self):
        return self.user_name + ' ' + self.member_name

    class Meta:
        ordering = ['user_name']


class BannedWord(models.Model):
    word = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.word
