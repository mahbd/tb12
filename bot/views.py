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
    res = requests.post(telegram_url, data=data).json()
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
    new_user = False
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
    member_id = 100
    user_name = 'none'
    BotAccessInfo.objects.get_or_create(type=chat_type, name=name, chat_id=chat_id)
    if chat_type == 'private':
        group = BotAccessInfo.objects.get(name='private')
    else:
        group = BotAccessInfo.objects.get(type=chat_type, name=name, chat_id=chat_id)
    try:
        member_id = data['message']['new_chat_member']['id']
        user_name = data['message']['new_chat_member']['username']
        new_user = True
        message_to_send = "Hey, You are now part of BRUR NewBies. Please send your online judge(codeforces, uri and vjudge) " \
                          "details to @mahmudula2000 so that I can see automically if you solved any problem. Remember If " \
                          "you don't send information, I couldn't know about your submission and will remove you " \
                          "from group after 72 hours"
        res = sm(message_to_send, member_id)
        rm(chat_id, message_id)
        print(res)
    except KeyError:
        pass
    try:
        member_id = data['message']['from']['id']
        user_name = data['message']['from']['username']
    except KeyError:
        pass
    MemberList.objects.get_or_create(member_id=member_id, user_name=user_name, group=group)
    if message == 'add_me':
        sm('added successfully', chat_id)
    elif message.find('=delete_above') != -1 and message.find('=delete_above') != 0:
        for m in range(int(message[0]) + 1):
            rm(chat_id, message_id - m)
    elif group.name == 'BRUR NewBees':

        try:
            BannedWord.objects.get(word=message.strip().lower())
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
            "chat_id": -370548956,
            "user_id": request.POST['user_id']
        }
        res = requests.post(telegram_url, data=data).json()
        return JsonResponse(res)
    context = {
        'details': MemberList.objects.filter(group__name='BRUR NewBees'),
        'title': 'remove user'
    }
    return render(request, 'bot/rmv_usr.html', context)
