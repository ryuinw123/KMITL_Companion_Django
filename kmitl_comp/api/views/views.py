# from urllib import response
# from django.core.exceptions import BadRequest
# from django.forms import ValidationError
# from django.http import HttpResponse, HttpResponseBadRequest
# from django.http import JsonResponse
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# import os

# from ..models import *

# ########

# import json
# import string
# import random
# import regex as re
# import datetime
# import requests

# #utils
# from ..utils import *

# import requests as req

# import jwt

# #nextcloud
# import nextcloud_client

# nc = nextcloud_client.Client('http://nextcloud.shitduck.duckdns.org/')
# nc.login('pokemon', 'Pokemon19!!')
# imagenumber = 0

#/*********************** import all method ********************/

import os
import importlib
import glob
#modnames = [".views_methods.Auth"]

modpath = [os.path.basename(x) for x in glob.glob(os.path.join(os.path.dirname(__file__), "views_methods/**"))]
modpath = [".views_methods."+path for path in modpath if path not in ["__init__.py","__pycache__"]]
modnames = modpath

for lib in modnames:
    #globals()[lib] = importlib.import_module(lib,package=__package__)
    exec(f'{lib.split(".")[-1]} = importlib.import_module(__package__ + lib)')
    # for symbol in module.__all__:
    #     globals()[symbol] = getattr(module, symbol)

#/*********************** end import all method ********************/

## non code here















# #/*********************** jwt encode decode method ********************/
# def jwtEncode(id,email,exp,iat):   
#     return jwt.encode({'id':id,'email':email,'exp':exp,'iat':iat},'secret', algorithm='HS256')

# def jwtDecode(token):
#     return jwt.decode(token, 'secret', algorithms=['HS256'])

# #/*************************** login method *****************************/

# def checkUserHaveDataFromId(student_id_) -> bool:
#     query = User.objects.all().filter(student_id=student_id_).values()
#     query_list = list(query)
#     return False if len(query) == 0 else True

# def callTokenFromId(student_id_):
#     query = User.objects.all().filter(student_id=student_id_).values()
#     query_list = list(query)
#     return query_list[0]['token']


# @csrf_exempt
# def getLocationQuery(request) -> None:
#     if request.method == "POST":
#         data = request.POST
#         latitude = data["latitude"]
#         longitude = data["longitude"]
#         x = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/{longitude},{latitude}.json?access_token=pk.eyJ1Ijoicnl1aW53MTIzIiwiYSI6ImNsODV5M21odjB0dXAzbm9lZDhnNXVoY2UifQ.IiTAr5ITOUcCVjPjWiRe1w&limit=1")
#         data = x.json()

#         if (data):
#             feature = data["features"][0]

#             response = {
#                 "place" : feature["text"],
#                 "address" : feature["place_name"]
#             }
#         else:
#             response = {
#                 "place" : " ",
#                 "address" : " "
#             }
        

#         return JsonResponse(response,safe=False)
    

# @csrf_exempt
# def userLogin(request) -> None:
#     if request.method == 'POST':
#         data_dict = request.POST
#         data_dict = dataRefacter(data_dict)
#         status = 0
        
#         #Authorization
#         authCode = data_dict['authCode']
#         returnToken = ""

#         if (len(authCode) <= 73) and len(authCode) != 0 :
#             all_token = google_get_access_token(authCode)
#             #google_refresh_token = "" ##need to fix
#             google_access_token = all_token['access_token']
#             user_data = google_get_data_from_token(google_access_token)

#             student_id_ = user_data['email'].split('@')[0]

#             if checkUserHaveDataFromId(student_id_) == True:
#                 status = 1
#                 returnToken = callTokenFromId(student_id_)
#             else:
#                 kmitl_token = jwtEncode(user_data['email'].split('@')[0],user_data['email'],datetime.datetime.utcnow() + datetime.timedelta(hours=525600),datetime.datetime.utcnow())
#                 returnToken = kmitl_token
            

#         else:
#             #print('loginwithtoken*',authCode,'*')
#             return userTokenLogin(request,authCode)

#         #     all_token = google_refresh_access_token(authCode)
#         #     google_refresh_token = authCode
#         #     print('false')

#         response = {
#             'status' : status,
#             'refreshToken' : returnToken,
#             'email': user_data['email']
#         }

#         return JsonResponse(response,safe=False)
#     raise BadRequest('This method not support GET request')

# def userTokenLogin(request,kmitl_token) -> None:
#     if request.method == 'POST':
#         #data_dict = request.POST
#         #data_dict = dataRefacter(data_dict)
#         #print(data_dict)

#         auth_status = 0
#         return_token = ""
#         return_email = ""
        
#         try:
#             decoded_data = jwtDecode(kmitl_token)
#         except Exception as e:
#             print("error " ,e)
#             return JsonResponse({'status' : auth_status,
#                                 'refreshToken' : return_token,
#                                 'email': return_email},safe=False)

        
        
#         query = User.objects.all().filter(student_id=decoded_data['id']).values()
#         lsquery = list(query)

#         if len(lsquery) != 0:
#             if (str(lsquery[0]['token']) == str(kmitl_token)) and (str(lsquery[0]['email']) == str(decoded_data['email'])):
#                 auth_status = 1
#                 return_token = kmitl_token
#                 return_email = decoded_data['email']

#         response = {
#             'status' : auth_status,
#             'refreshToken' : return_token,
#             'email': return_email
#         }

#         return JsonResponse(response,safe=False)

#     raise BadRequest('This method not support GET request')

# def google_get_access_token(code: str) -> str:
#     # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
#     data = {
#         'code': code,
#         'client_id': GoogleAuthConsoleData().client_id,
#         'client_secret': GoogleAuthConsoleData().client_secret,
#         'redirect_uri': GoogleAuthConsoleData().redirect_url,
#         'grant_type': 'authorization_code'
#     }
#     response = req.post("https://oauth2.googleapis.com/token", data=data)
#     if not response.ok:
#         raise ValidationError('Failed to obtain access token from Google.')
#     token = response.json()
#     print("access token",token['access_token'])

#     return token

# def google_refresh_access_token(refresh_token: str) -> str:
#     data = {
#         'client_id': GoogleAuthConsoleData().client_id,
#         'client_secret': GoogleAuthConsoleData().client_secret,
#         'grant_type': 'refresh_token',
#         'refresh_token' : refresh_token
#     }
#     response = req.post("https://oauth2.googleapis.com/token", data=data)
#     if not response.ok:
#         raise ValidationError('Failed to obtain access token from Google with refresh token.')
#     token = response.json()
#     print(token['access_token'])
#     return token

# def google_get_data_from_token(access_token: str) -> str:
#     data = {
#         'Authorization': 'Bearer ' + access_token
#     }
    
#     response = req.get("https://www.googleapis.com/oauth2/v2/userinfo",headers=data)
#     print(response.json())
  
#     if not response.ok:
#         raise ValidationError('Failed to obtain data from Google.')
#     auth_userdata = response.json()
#     hd = auth_userdata['email'].split('@')[-1]
#     if hd != "kmitl.ac.th":
#         raise ValidationError('Can obtain data from With Kmitl Account Only.')

#     # hd = auth_userdata['email'].split('@')[-1]
#     # AuthDataStore().name = auth_userdata['name']
#     # AuthDataStore().email = auth_userdata['email']
#     # AuthDataStore().given_name = auth_userdata['given_name']
#     # AuthDataStore().family_name = auth_userdata['family_name']
#     # AuthDataStore().hd = hd

#     return auth_userdata

# @csrf_exempt
# def postUserData(request) -> None:
#     if request.method == 'POST':
#         data_dict = request.POST
#         data_dict = dataRefacter(data_dict)
#         try:
#             decode_token = jwtDecode(data_dict['authCode'])
#         except Exception as e:
#             raise e
#         #saveData(data_dict,student_id_)

#         try:
#             query = User(student_id=decode_token['id'],
#                         firstname=data_dict['name'],
#                         lastname=data_dict['surname'],
#                         email=decode_token['email'],
#                         token=data_dict['authCode'],
#                         faculty=data_dict['faculty'],
#                         department=data_dict['department'],
#                         year= int(data_dict['year']) )
#             query.save()
#             return HttpResponse('Save Success !!!')
#         except Exception as e:
#             raise e

#     raise BadRequest('This method not support GET request')
        
#def saveData(data_dict,student_id_):

# #/********************************* test method ********************************/

# testlst = [{
#     "id":30,
#     "latitude":"13.779677724153272" ,
#     "longitude" : "100.67650630259816",
#     "description" : "noob",
#     "address" : "9/35 how",
#     "place":"Tun School",
#     "type" : "School",
#     "imageLink": ["https://m.media-amazon.com/images/G/01/gc/designs/livepreview/a_generic_white_10_us_noto_email_v2016_us-main._CB627448186_.png","https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2Fbbdd464a-04e2-4a5a-8cbe-198465d68fdb.jpg?fit=scale-down&source=next&width=700"]},
#     {"place":"Cena",
#     "id":31,
#     "latitude":"13.779677724153272",
#     "longitude" : "100.97650630259816",
#     "description" : "noob2",
#     "address" : "How the heck",
#     "place" : "TunnelSchool",
#     "type" : "Pokemon",
#     "imageLink":["https://pbs.twimg.com/profile_images/1250516096907571200/adjxWadZ_400x400.jpg"]
#     }]


# def helloWorld(request):
#     print(testlst)

#     return JsonResponse(testlst,safe = False)


# @api_view(['POST'])
# def testpost(request):
#     print(request.data)
#     if request.method == 'POST':
#         global imagenumber
#         data_dict = request.POST
#         name = data_dict["name"]
#         detail = data_dict["detail"]
#         tag = data_dict["type"]
#         file = request.data['image'] # or self.files['image'] in your form
#         path = default_storage.save(f'tmp/image.png', ContentFile(file.read()))
#         tmp_file = os.path.join(settings.MEDIA_ROOT, path)
#         print(tmp_file)
        
#         print(data_dict)

#         latitude = data_dict['latitude']
#         longitude = data_dict['longitude']
#         nc.put_file(f"KMITLcompanion/image{imagenumber}.png",tmp_file)
#         link_info = nc.share_file_with_link(f'KMITLcompanion/image{imagenumber}.png')
#         imagenumber = imagenumber+1
#         link = link_info.get_link() + "/preview"
#         print(link)
#         testlst.append({"place":name, "id":random.randint(1000,2000), "latitude":latitude , "longitude" : longitude,"description" : "noob2" , "address" : detail , "type" : tag , "imageLink" : [link]})
#         return HttpResponse()

# @csrf_exempt
# def checkToken(request):

#     return HttpResponse('')

    
# @csrf_exempt
# def testToken(request):
#     if request.method == 'POST':
#         token = json.loads(request.body)['token']
#         print(token)

#         response_data = {}
#         response_data['token'] = token

#         return HttpResponse(json.dumps(response_data), content_type="application/json")


