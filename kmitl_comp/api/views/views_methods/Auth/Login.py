from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.core.exceptions import BadRequest
import jwt
from django.views.decorators.csrf import csrf_exempt
from django.forms import ValidationError
from datetime import datetime
from datetime import timedelta

import requests as req

from ....models import *

#utils
from ....utils import *

#/*********************** jwt encode decode method ********************/
def jwtEncode(id,email,exp,iat):   
    return jwt.encode({'id':id,'email':email,'exp':exp,'iat':iat},'secret', algorithm='HS256')

def jwtDecode(token):
    return jwt.decode(token, 'secret', algorithms=['HS256'])

#/*************************** login method *****************************/

def checkUserHaveDataFromId(student_id_) -> bool:
    query = User.objects.all().filter(student_id=student_id_).values()
    query_list = list(query)
    return False if len(query) == 0 else True

def callTokenFromId(student_id_):
    query = User.objects.all().filter(student_id=student_id_).values()
    query_list = list(query)
    return query_list[0]['token']

@csrf_exempt
def userLogin(request) -> None:
    if request.method == 'POST':
        data_dict = request.POST
        data_dict = dataRefacter(data_dict)
        status = 0
        
        #Authorization
        authCode = data_dict['authCode']
        returnToken = ""

        if (len(authCode) <= 73) and len(authCode) != 0 :
            all_token = google_get_access_token(authCode)
            #google_refresh_token = "" ##need to fix
            google_access_token = all_token['access_token']
            user_data = google_get_data_from_token(google_access_token)

            student_id_ = user_data['email'].split('@')[0]

            if checkUserHaveDataFromId(student_id_) == True:
                status = 1
                returnToken = callTokenFromId(student_id_)
            else:
                kmitl_token = jwtEncode(user_data['email'].split('@')[0],user_data['email'],datetime.utcnow() + timedelta(hours=525600),datetime.utcnow())
                returnToken = kmitl_token
            

        else:
            #print('loginwithtoken*',authCode,'*')
            return userTokenLogin(request,authCode)

        #     all_token = google_refresh_access_token(authCode)
        #     google_refresh_token = authCode
        #     print('false')

        response = {
            'status' : status,
            'refreshToken' : returnToken,
            'email': user_data['email']
        }

        return JsonResponse(response,safe=False)
    raise BadRequest('This method not support GET request')

def userTokenLogin(request,kmitl_token) -> None:
    if request.method == 'POST':
        #data_dict = request.POST
        #data_dict = dataRefacter(data_dict)
        #print(data_dict)

        auth_status = 0
        return_token = ""
        return_email = ""
        
        try:
            decoded_data = jwtDecode(kmitl_token)
        except Exception as e:
            print("error " ,e)
            return JsonResponse({'status' : auth_status,
                                'refreshToken' : return_token,
                                'email': return_email},safe=False)

        
        
        query = User.objects.all().filter(student_id=decoded_data['id']).values()
        lsquery = list(query)

        if len(lsquery) != 0:
            if (str(lsquery[0]['token']) == str(kmitl_token)) and (str(lsquery[0]['email']) == str(decoded_data['email'])):
                auth_status = 1
                return_token = kmitl_token
                return_email = decoded_data['email']

        response = {
            'status' : auth_status,
            'refreshToken' : return_token,
            'email': return_email
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
    if hd != "kmitl.ac.th":
        raise ValidationError('Can obtain data from With Kmitl Account Only.')

    # hd = auth_userdata['email'].split('@')[-1]
    # AuthDataStore().name = auth_userdata['name']
    # AuthDataStore().email = auth_userdata['email']
    # AuthDataStore().given_name = auth_userdata['given_name']
    # AuthDataStore().family_name = auth_userdata['family_name']
    # AuthDataStore().hd = hd

    return auth_userdata

@csrf_exempt
def postUserData(request) -> None:
    if request.method == 'POST':
        data_dict = request.POST
        data_dict = dataRefacter(data_dict)
        try:
            decode_token = jwtDecode(data_dict['authCode'])
        except Exception as e:
            raise e
        #saveData(data_dict,student_id_)

        try:
            query = User(student_id=decode_token['id'],
                        firstname=data_dict['name'],
                        lastname=data_dict['surname'],
                        email=decode_token['email'],
                        token=data_dict['authCode'],
                        faculty=data_dict['faculty'],
                        department=data_dict['department'],
                        year= int(data_dict['year']) )
            query.save()
            return HttpResponse('Save Success !!!')
        except Exception as e:
            raise e

    raise BadRequest('This method not support GET request')