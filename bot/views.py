import json
from django.http import HttpResponse
from .models import BotAccessInfo


def bot_get(request):
    data = json.loads(request.body)
    print(data)
    try:
        chat_type = data['message']['chat']['chat_type']
    except KeyError:
        return HttpResponse("Success")
    try:
        message = data['message']['text']
    except KeyError:
        message = "A file shared"
    chat_id = data['message']['chat']['id']
    if chat_type == 'group':
        name = data['message']['chat']['title']
    else:
        try:
            fn = data['message']['from']['first_name']
        except KeyError:
            fn = " "
        try:
            ln = data['message']['from']['last_name']
        except KeyError:
            ln = " "
        name = fn + ' ' + ln
    BotAccessInfo.objects.get_or_create(type=chat_type, name=name, chat_id=chat_id)
    BotAccessInfo.objects.get(type=chat_type, name=name, chat_id=chat_id)
    '''
    telegram_url = "https://api.telegram.org/bot"
    tutorial_bot_token = "1214433734:AAGgKkYrFuiMSXmRNoUmVPvaBUD9HVVgVuM"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    requests.post(
        f"{telegram_url}{tutorial_bot_token}/sendMessage", data=data
    )
    '''
    return HttpResponse("Success")
