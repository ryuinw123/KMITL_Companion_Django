from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt

#oauth
from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = "27567133155-3gsequ5o2m08cnj6vnqgdllkv7tabobg.apps.googleusercontent.com"

#get
def helloWorld(request):
    x = [{"name":"John", "id":30, "latitude":"13.779677724153272" , "longitude" : "100.67650630259816","description" : "noob"} , {"name":"Cena", "id":31, "latitude":"13.779677724153272" , "longitude" : "100.97650630259816","description" : "noob2"}]

    return JsonResponse(x,safe = False)
    #user = User.objects.all()[0].student_id
    #return HttpResponse(user)

@csrf_exempt
def checkToken(request):
    if request.method == 'POST':

        token = json.loads(request.body)['token']
        request = requests.Request()

        ####
        response_data = {}

        try:
            id_info = id_token.verify_oauth2_token(token, request, CLIENT_ID)

            auth_userdata = id_info

            response_data = {}
            response_data['token'] = token
            response_data['auth_userdata'] = str(auth_userdata)
            response_data['validate'] = True
            print(response_data)

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:

            response_data['validate'] = False
            print(e)
            return HttpResponse(json.dumps(response_data), content_type="application/json")


      
@csrf_exempt
def testToken(request):
    if request.method == 'POST':
        token = json.loads(request.body)['token']
        print(token)

        response_data = {}
        response_data['token'] = token

        return HttpResponse(json.dumps(response_data), content_type="application/json")

