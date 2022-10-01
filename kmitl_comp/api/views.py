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
        try:
            token = json.loads(request.body)['token']

            print(token)
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            
            response_data = {}
            response_data['token'] = token
            response_data['sub'] = userid
            print(response_data)

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except ValueError:
            # Invalid token
            return "error"
        