from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def default_view(request):
    html = "<h1>Hello from default view</h1>"
    return HttpResponse(html)