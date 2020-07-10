import json

import requests
from django.http import HttpResponse
from django.shortcuts import render

from .models import BotAccessInfo


def bot_get(request):
    data = json.loads(request.body)
    try:
        chat_type = data['message']['chat']['type']
    except KeyError:
        return HttpResponse("Success")
    try:
        message = data['message']['text']
    except KeyError:
        message = "A file shared"
    chat_id = data['message']['chat']['id']
    if chat_type == 'group' or chat_type == 'super_group':
        name = data['message']['chat']['title']
    else:
        try:
            name = data['message']['from']['username']
        except KeyError:
            name = 'not_found'
    BotAccessInfo.objects.get_or_create(type=chat_type, name=name, chat_id=chat_id)
    if message == 'add_me':
        telegram_url = "https://api.telegram.org/bot"
        tutorial_bot_token = "1214433734:AAGgKkYrFuiMSXmRNoUmVPvaBUD9HVVgVuM"
        data = {
            "chat_id": chat_id,
            "text": 'Added successfully.',
            "parse_mode": "Markdown",
        }
        requests.post(
            f"{telegram_url}{tutorial_bot_token}/sendMessage", data=data
        )
    print(data)
    return HttpResponse("Success")


def send_tm(request):
    if request.method == 'POST':
        telegram_url = "https://api.telegram.org/bot"
        tutorial_bot_token = "1214433734:AAGgKkYrFuiMSXmRNoUmVPvaBUD9HVVgVuM"
        data = {
            "chat_id": request.POST['chat_id'],
            "text": request.POST['message'],
            "parse_mode": "Markdown",
        }
        requests.post(
            f"{telegram_url}{tutorial_bot_token}/sendMessage", data=data
        )
        return HttpResponse("message sent")
    else:
        details = BotAccessInfo.objects.all()
        context = {
            'title': 'send_message',
            'details': details,
        }
        return render(request, 'bot/send_tm.html', context)
