from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.core.mail import send_mail


def index(request):
    # print('hello')
    send_mail(
        'test',
        'hello',
        'sale@weestep.pl',
        ['buzovskiy.v@gmail.com']
    )
    return HttpResponse('output')
