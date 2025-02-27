from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from users.models import CustomUser



# Create your views here.

def login(request):
    return render(request, 'login_templates/login.html')

def signup(request):
    return render(request, 'login_templates/sign_up.html')

def home(request):
    return render(request, 'webpages/home.html')

def watch(request):
    return render(request, 'webpages/video.html')


