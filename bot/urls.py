from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from bot import views

app_name = 'bot'
urlpatterns = [
    path('get/', csrf_exempt(views.bot_get), name='get'),
]
