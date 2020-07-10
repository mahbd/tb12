import json
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import BotAccessInfo, MemberList, BannedWord
from tb12.settings import BOT_ACCESS_TOKEN


def sm(text, chat_id):
    telegram_url = 'https://api.telegram.org/bot' + BOT_ACCESS_TOKEN + 'sendMessage'
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    res = requests.post(telegram_url, data=data)
    return res


def rm(chat_id, message_id):
    telegram_url = 'https://api.telegram.org/bot' + BOT_ACCESS_TOKEN + '/deleteMessage'
    data = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    res = requests.post(telegram_url, data=data)
    print(res)


def bot_get(request):
    data = json.loads(request.body)
    try:
        chat_type = data['message']['chat']['type']
    except KeyError:
        return HttpResponse("Success")
    try:
        message = data['message']['text']
    except KeyError:
        message = "ErrorHappenedInBot"
    chat_id = data['message']['chat']['id']
    message_id = data['message']['message_id']
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
        rm(chat_id, message_id)
    except KeyError:
        member_id = data['message']['from']['id']
        user_name = data['message']['from']['username']
    MemberList.objects.get_or_create(member_id=member_id, user_name=user_name, group=group)
    if message == 'add_me':
        sm('added successfully', chat_id)
    elif message.find('=delete_above') != -1 and message.find('=delete_above') != 0:
        for m in range(int(message[0] + 1)):
            rm(chat_id, message_id - m)
    elif group.name == 'test_bot':
        try:
            BannedWord.objects.get(word=message.strip())
            message_id = data['message']['message_id']
            rm(chat_id, message_id)
        except BannedWord.DoesNotExist:
            pass
        except BannedWord.MultipleObjectsReturned:
            message_id = data['message']['message_id']
            rm(chat_id, message_id)
    print(data)
    return HttpResponse("Success")


def send_tm(request):
    if request.method == 'POST':
        res = sm(request.POST['message'], request.POST['chat_id'])
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
        telegram_url = "https://api.telegram.org/bot" + BOT_ACCESS_TOKEN + "/kickChatMember"
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
