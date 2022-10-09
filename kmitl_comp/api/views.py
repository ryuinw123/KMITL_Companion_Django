from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
import json

from h11 import ERROR
from .models import *
from django.views.decorators.csrf import csrf_exempt

import string
import random

#oauth
from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = "563509002084-b7m05boiaqs5mo0thi4ka59noiakeus2.apps.googleusercontent.com"


testlst = [{"name":"John", "id":30, "latitude":"13.779677724153272" , "longitude" : "100.67650630259816","description" : "noob"},{"name":"Cena", "id":31, "latitude":"13.779677724153272" , "longitude" : "100.97650630259816","description" : "noob2"}]
def helloWorld(request):
    print(testlst)

    return JsonResponse(testlst,safe = False)

def testpost(request):
    if request.method == 'POST':
        data_dict = request.POST
        print(data_dict)
        #json_dict = json.loads(request.data)
        #print(json_dict)
        letters = string.ascii_lowercase
        randomword = ''.join(random.choice(letters) for i in range(9))
        latitude = data_dict['latitude']
        longitude = data_dict['longitude']
        testlst.append({"name":randomword, "id":random.randint(1000,2000), "latitude":latitude , "longitude" : longitude,"description" : "noob2"})
        print(testlst)
        return HttpResponse('')

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

        print("token",token)

        ####
        response_data = {}

        try:
            id_info = id_token.verify_oauth2_token(token, request, CLIENT_ID)

            auth_userdata = id_info

            response_data = {}
            response_data['token'] = token
            response_data['auth_userdata'] = str(auth_userdata)
            response_data['validate'] = True
            print("response data ",response_data)

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:

            print(e)
            return HttpResponseBadRequest


      
@csrf_exempt
def testToken(request):
    if request.method == 'POST':
        token = json.loads(request.body)['token']
        print(token)

        response_data = {}
        response_data['token'] = token

        return HttpResponse(json.dumps(response_data), content_type="application/json")

