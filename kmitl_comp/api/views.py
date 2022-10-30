from urllib import response
from django.core.exceptions import BadRequest
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *

########

import json
import string
import random
import regex as re


#utils
from .utils import *

import requests as req


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
        status = 0
        
        #Authorization
        
        authCode = data_dict['authCode'][1:-1]

        if len(authCode) <= 73:
            all_token = google_get_access_token(authCode)
            refresh_token = "" ##need to fix
        else:
            all_token = google_refresh_access_token(authCode)
            refresh_token = authCode
            print('false')

        access_token = all_token['access_token']

        google_get_data_from_token(access_token)

        if checkUserHaveData() == True:
            status = 1

        response = {
            'status' : status,
            'refreshToken' : access_token,
            'email': AuthDataStore().email
        }

        return JsonResponse(response,safe=False)
    raise BadRequest('This method not support GET request')

def google_get_access_token(code: str) -> str:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
    data = {
        'code': code,
        'client_id': GoogleAuthConsoleData().client_id,
        'client_secret': GoogleAuthConsoleData().client_secret,
        'redirect_uri': GoogleAuthConsoleData().redirect_url,
        'grant_type': 'authorization_code'
    }
    response = req.post("https://oauth2.googleapis.com/token", data=data)
    if not response.ok:
        raise ValidationError('Failed to obtain access token from Google.')
    token = response.json()
    print("access token",token['access_token'])

    return token

def google_refresh_access_token(refresh_token: str) -> str:
    data = {
        'client_id': GoogleAuthConsoleData().client_id,
        'client_secret': GoogleAuthConsoleData().client_secret,
        'grant_type': 'refresh_token',
        'refresh_token' : refresh_token
    }
    response = req.post("https://oauth2.googleapis.com/token", data=data)
    if not response.ok:
        raise ValidationError('Failed to obtain access token from Google with refresh token.')
    token = response.json()
    print(token['access_token'])

    return token

def google_get_data_from_token(access_token: str) -> str:
    data = {
        'Authorization': 'Bearer ' + access_token
    }
    
    response = req.get("https://www.googleapis.com/oauth2/v2/userinfo",headers=data)
    print(response.json())
  
    if not response.ok:
        raise ValidationError('Failed to obtain data from Google.')
    auth_userdata = response.json()

    hd = auth_userdata['email'].split('@')[-1]
    AuthDataStore().name = auth_userdata['name']
    AuthDataStore().email = auth_userdata['email']
    AuthDataStore().given_name = auth_userdata['given_name']
    AuthDataStore().family_name = auth_userdata['family_name']
    AuthDataStore().hd = hd

    return auth_userdata



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

