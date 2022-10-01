from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt

#oauth
from google.oauth2 import id_token
from google.auth.transport import requests

# Create your views here.

CLIENT_ID = "27567133155-3gsequ5o2m08cnj6vnqgdllkv7tabobg.apps.googleusercontent.com"

#get
def helloWorld(request):
    user = User.objects.all()[0].student_id


    return HttpResponse(user)

@csrf_exempt
def testToken(request):
    if request.method == 'POST':
        token = json.loads(request.body)['token']
        print(token)

        response_data = {}
        response_data['token'] = token

        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def checkToken(request):
    if request.method == 'POST':

        token = json.loads(request.body)['token']
        request = requests.Request()

        id_info = id_token.verify_oauth2_token(token, request, '27567133155-3gsequ5o2m08cnj6vnqgdllkv7tabobg.apps.googleusercontent.com')

        auth_userdata = id_info


        response_data = {}
        response_data['token'] = token
        response_data['sub'] = str(auth_userdata)
        print(response_data)

        return HttpResponse(json.dumps(response_data), content_type="application/json")

        