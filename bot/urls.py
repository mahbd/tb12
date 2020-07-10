from django.urls import path

from bot import views

app_name = 'bot'
urlpatterns = [
    path('get/', views.bot_get, name='get'),
]
