from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Author working')

# Create your views here.
