from django.core.exceptions import BadRequest
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import random
import json

# #/********************************* nextcloud method ********************************/

# #nextcloud
# import nextcloud_client

# nc = nextcloud_client.Client('http://nextcloud.shitduck.duckdns.org/')
# nc.login('pokemon', 'Pokemon19!!')
# imagenumber = 0

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
