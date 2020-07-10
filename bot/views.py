import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import BotAccessInfo, MemberList


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
    if chat_type == 'group' or chat_type == 'supergroup':
        name = data['message']['chat']['title']
    else:
        try:
            name = data['message']['from']['username']
        except KeyError:
            name = 'not_found'
    BotAccessInfo.objects.get_or_create(type=chat_type, name=name, chat_id=chat_id)
    if chat_type == 'private':
        group = BotAccessInfo.objects.get(name='private')
    else:
        group = BotAccessInfo.objects.get(type=chat_type, name=name, chat_id=chat_id)
    try:
        member_id = data['message']['new_chat_member']['id']
        user_name = data['message']['new_chat_member']['username']
    except KeyError:
        member_id = data['message']['from']['id']
        user_name = data['message']['from']['username']
    MemberList.objects.get_or_create(member_id=member_id, user_name=user_name, group=group)
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
        telegram_url = "https://api.telegram.org/bot1214433734:AAGgKkYrFuiMSXmRNoUmVPvaBUD9HVVgVuM/sendMessage"
        data = {
            "chat_id": request.POST['chat_id'],
            "text": request.POST['message'],
            "parse_mode": "Markdown",
        }
        res = requests.post(telegram_url, data=data)
        return JsonResponse(res)
    else:
        details = BotAccessInfo.objects.all()
        context = {
            'title': 'send_message',
            'details': details,
        }
        return render(request, 'bot/send_tm.html', context)


def rmv_usr(request):
    if request.method == 'POST':
        telegram_url = "https://api.telegram.org/bot1214433734:AAGgKkYrFuiMSXmRNoUmVPvaBUD9HVVgVuM/kickChatMember"
        data = {
            "chat_id": -460276901,
            "user_id": request.POST['user_id']
        }
        res = requests.post(telegram_url, data=data).json()
        return JsonResponse(res)
    context = {
        'details': MemberList.objects.filter(group__name='bot_test'),
        'title': 'remove user'
    }
    return render(request, 'bot/rmv_usr.html', context)
