from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponse


def get_csrf(request):
    x = csrf(request)
    csrf_token = x['csrf_token']
    return HttpResponse(csrf_token)


def graph_demo(request):
    header_content = 'Network Graph View Demo'
    return render(request, 'graph_demo.html', {'header_content': header_content})
