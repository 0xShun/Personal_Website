from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Wassup")

def blog(request):
    return HttpResponse("<h1>Welcome To My Blog!!</h1>")

def projects(request):
    return HttpResponse("Github Projects Here")