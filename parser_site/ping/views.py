from django.http import HttpResponse


def index(request):
    return HttpResponse('Pong. Site is working now')
