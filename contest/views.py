from django.http import HttpResponse
from django.shortcuts import render
import os


def run_file():
    if os.system("g++ out.cpp -o out") == 0:
        if os.system("timeout --preserve-status 1 ./out < test_in.txt > program_out.txt") != 0:
            return "TLE"
        else:
            if os.system("diff program_out.txt test_out.txt") == 0:
                return "AC"
            else:
                return "WA"
    else:
        return "CE"


def test(request):
    res = run_file()
    return HttpResponse(res)