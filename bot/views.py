import json
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import BotAccessInfo, MemberList, BannedWord, BotMessage
from tb12.settings import BOT_ACCESS_TOKEN


def error_handle(data, key):
    try:
        res = data[key]
    except:
        res = '0'
    if res == '':
        res = '0'
    return res


def name_handle(data):
    user_details = []
    try:
        new = data['new_chat_member']
        try:
            fn = new['first_name']
            if fn == '' or fn is None:
                fn = '0'
        except KeyError:
            fn = '0'
        try:
            ln = new['last_name']
            if ln == '' or ln is None:
                ln = '0'
        except KeyError:
            ln = '0'
        try:
            user_name = new['username']
            if user_name == '' or user_name == None:
                user_name = '0'
        except KeyError:
            user_name = '0'
        try:
            user_id = new['id']
            if user_id == '' or user_id is None:
                user_id = '0'
        except KeyError:
            user_id = '0'
    except KeyError:
        try:
            fn = data['from']['first_name']
            if fn == '' or fn is None:
                fn = '0'
        except KeyError:
            fn = '0'
        try:
            ln = data['from']['last_name']
            if ln == '' or ln is None:
                ln = '0'
        except KeyError:
            ln = '0'
        try:
            user_name = data['from']['username']
            if user_name == '' or user_name is None:
                user_name = '0'
        except KeyError:
            user_name = '0'
        try:
            user_id = data['from']['id']
            if user_id == '' or user_id is None:
                user_id = '0'
        except KeyError:
            user_id = '0'
    user_details.append(fn + ' ' + ln)
    user_details.append(user_id)
    user_details.append(user_name)
    return user_details


def extract_tm(data):
    try:
        data = data['message']

    except KeyError:
        to_send = {'terminate': True}
        return to_send
    chat = data['chat']
    user_details = name_handle(data)
    try:
        new_user = data['new_chat_member']
        if new_user:
            new_user = True
        else:
            new_user = False
    except KeyError:
        new_user = False
    try:
        group_name = chat['title']
        is_group = True
    except KeyError:
        group_name = '0'
        is_group = False
    to_send = {'terminate': False,
               'message_id': int(error_handle(data, 'message_id')),
               'message': error_handle(data, 'text').strip().lower(),
               'chat_id': int(error_handle(chat, 'id')),
               'chat_type': error_handle(chat, 'type'),
               'name': user_details[0],
               'user_id': int(user_details[1]),
               'username': user_details[2],
               'new_user': new_user,
               'group_name': group_name,
               'is_group': is_group,
               }
    return to_send


def save_to_database(data):
    BotMessage.objects.create(message_id=data['message_id'], message=data['message'], chat_id=str(data['chat_id']),
                              chat_type=data['chat_type'], name=data['name'], user_id=data['user_id'],
                              username=data['username'], group_name=data['group_name'])


def sm(text, chat_id):
    telegram_url = 'https://api.telegram.org/bot' + BOT_ACCESS_TOKEN + '/sendMessage'
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    res = requests.post(telegram_url, data=data).json()
    print(res)
    return res


def rm(chat_id, message_id):
    telegram_url = 'https://api.telegram.org/bot' + BOT_ACCESS_TOKEN + '/deleteMessage'
    data = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    res = requests.post(telegram_url, data=data).json()
    print(res)


def bot_get(request):
    data = json.loads(request.body)
    data = extract_tm(data)
    if data['terminate']:
        return HttpResponse("Success")
    if data['is_group']:
        BotAccessInfo.objects.get_or_create(type=data['chat_type'], name=data['group_name'], chat_id=data['chat_id'])
        group = BotAccessInfo.objects.get(name=data['group_name'], chat_id=data['chat_id'])
        MemberList.objects.get_or_create(member_id=data['user_id'], user_name=data['username'],
                                         member_name=data['name'])
        MemberList.objects.get(member_id=data['user_id']).group.add(group)
    else:
        MemberList.objects.get_or_create(member_id=data['user_id'], user_name=data['username'],
                                         member_name=data['name'])
    if data['group_name'] == 'BRUR NewBees' or data['group_name'] == 'bot_test':
        if data['new_user']:
            mts = "Hey, You are now part of BRUR NewBies. Please send your online judge(codeforces, uri and vjudge) " \
                  "details to @mahmudula2000 so that I can see automically if you solved any problem. Remember If " \
                  "you don't send information, I couldn't know about your submission and will remove you " \
                  "from group after 72 hours. If already sent, no need to send again."
            sm(mts, data['user_id'])
            rm(data['chat_id'], data['message_id'])
            try:
                BannedWord.objects.get(word=data['message'])
                rm(data['chat_id'], data['message_id'])
                sm("Your message contains banned sentence, so auto deleted", data['user_id'])
            except BannedWord.DoesNotExist:
                pass
            except BannedWord.MultipleObjectsReturned:
                rm(data['chat_id'], data['message_id'])
                sm("Your message contains banned sentence, so auto deleted", data['user_id'])
    if data['message'] == 'add_me':
        sm("added successfully", data['chat_id'])
    if data['message'].find('=delete_above') != -1 and data['message'].find('=delete_above') != 0:
        amount_del = int(data['message'][:int(data['message'].find('=delete_above'))]) + 1
        if amount_del <= 21:
            for ext_mid in range(amount_del):
                rm(data['chat_id'], int(data['message_id']) - ext_mid)
            sm("removed_successfully", int(data['user_id']))
        else:
            rm(data['chat_id'], data['message_id'])
            sm("can't delete more than 20", data['user_id'])
    print(data)
    save_to_database(data)
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
