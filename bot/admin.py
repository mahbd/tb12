from django.contrib import admin
from .models import BotAccessInfo, MemberList, BannedWord, BotMessage


admin.site.register(BotAccessInfo)
admin.site.register(MemberList)
admin.site.register(BannedWord)
admin.site.register(BotMessage)
