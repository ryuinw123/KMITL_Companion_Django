from django.core.exceptions import BadRequest
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *

########

import json
import string
import random
import regex as re


#oauth
from google.oauth2 import id_token
from google.auth.transport import requests

#utils
from .utils import *


#/*************************** login method *****************************/

def checkUserHaveData() -> bool:
    student_id_ = AuthDataStore().email.split('@')[0]
    query = User.objects.all().filter(student_id=student_id_).values()
    query_list = list(query)

    return False if len(query) == 0 else True


@csrf_exempt
def userLogin(request) -> None:
    if request.method == 'POST':
        data_dict = request.POST
        response = 0
        
        if checkUserHaveData() == True:
            response = 1

        return HttpResponse(response)
    raise BadRequest('This method not support GET request')


@csrf_exempt
def postUserData(request) -> None:
    if request.method == 'POST':
        data_dict = request.POST
        data_dict = dataRefacter(data_dict)
        print(data_dict)
        student_id_ = AuthDataStore().email.split('@')[0]

        try:
            query = User(student_id=student_id_,
                        firstname=data_dict['name'],
                        lastname=data_dict['surname'],
                        email=AuthDataStore().email,
                        token=data_dict['token'],
                        faculty=data_dict['faculty'],
                        department=data_dict['department'],
                        year= int(data_dict['year']) )
            query.save()
            return HttpResponse('Save Success !!!')
        except Exception as e:
            raise e
    raise BadRequest('This method not support GET request')
        


#/********************************* test method ********************************/

testlst = [{"name":"John", "id":30, "latitude":"13.779677724153272" , "longitude" : "100.67650630259816","description" : "noob"},{"name":"Cena", "id":31, "latitude":"13.779677724153272" , "longitude" : "100.97650630259816","description" : "noob2"}]
def helloWorld(request):
    print(testlst)

    return JsonResponse(testlst,safe = False)
    
@csrf_exempt
def testpost(request):
    if request.method == 'POST':
        data_dict = request.POST
        print(data_dict)

        letters = string.ascii_lowercase
        randomword = ''.join(random.choice(letters) for i in range(9))
        latitude = data_dict['latitude']
        longitude = data_dict['longitude']
        testlst.append({"name":randomword, "id":random.randint(1000,2000), "latitude":latitude , "longitude" : longitude,"description" : "noob2"})
        print(testlst)
        return HttpResponse('')

@csrf_exempt
def checkToken(request):

    return HttpResponse('')

    
@csrf_exempt
def testToken(request):
    if request.method == 'POST':
        token = json.loads(request.body)['token']
        print(token)

        response_data = {}
        response_data['token'] = token

        return HttpResponse(json.dumps(response_data), content_type="application/json")

