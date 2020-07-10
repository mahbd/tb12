from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup


def last_submission(request):
    handle_list = {'mah_python': 'Mahmudul Alam','shakib112': 'Shakib Hossain Shanto',
                    'MILOY': 'S.M. Miloy', 'nawab69':'Kibria', 'rakibnsajib1': 'Rakib Hossain Sajeeb'}
    res = "<p>last submission details</p>"
    for handle in handle_list:
        url = 'https://codeforces.com/submissions/' + handle + '/page/1'
        response = requests.get(url).content
        page = BeautifulSoup(response, 'html.parser')
        fn = page.findAll('tr')[26].findAll('td', attrs={'class': 'status-small'})[0].text.strip()
        fn = fn[:12] + str(int(fn[12:14]) + 3) + fn[14:]
        res += "<p>" + handle_list[handle] + "--->" + fn + "</p>"
    return HttpResponse(res)
