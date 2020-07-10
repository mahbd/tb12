from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup


def test(request):
    url = 'https://codeforces.com/submissions/mah_python/page/1'
    response = requests.get(url).content
    page = BeautifulSoup(response, 'html.parser')
    fn = page.findAll('tr')[26].findAll('td', attrs={'class': 'status-small'})[0].text
    return HttpResponse(fn)
