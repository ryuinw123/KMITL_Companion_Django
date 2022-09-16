from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def helloWorld(request):
    user = User.objects.all()[0].student_id


    return HttpResponse(user)
