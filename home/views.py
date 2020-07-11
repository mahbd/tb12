from django.http import Http404, HttpResponse
from django.shortcuts import render
from bot.models import BannedWord


def home(request):
    raise Http404


def abd(request):
    if request.method == 'POST':
        BannedWord.objects.get_or_create(word=str(request.POST['word']).strip().lower())
    context = {
        'title': 'banned word',
        'words': BannedWord.objects.all(),
    }
    return render(request, 'home/banned_word.html', context)
