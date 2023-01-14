
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.core.files.base import ContentFile
import random
import json
import ast

from ....models import *

#utils
from ....utils import *
#/********************************* nextcloud method ********************************/

#nextcloud
import nextcloud_client

nc = nextcloud_client.Client('http://nextcloud.shitduck.duckdns.org/')
nc.login('pokemon', 'Pokemon19!!')
imagenumber = 0

#/********************************* test method ********************************/

# testlst = [
#     {
#     'id':30,
#     'latitude':'59.29011536' ,
#     'longitude' : '18.02803609',
#     'description' : 'noob',
#     'address' : '9/35 how',
#     'place':'Tun School',
#     'type' : 'School',
#     'imageLink': ['https://m.media-amazon.com/images/G/01/gc/designs/livepreview/a_generic_white_10_us_noto_email_v2016_us-main._CB627448186_.png','https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2Fbbdd464a-04e2-4a5a-8cbe-198465d68fdb.jpg?fit=scale-down&source=next&width=700']},
#     {"id":31,
#     "latitude":"0",
#     "longitude" : "0",
#     "description" : 'noob2xxxxxxx',
#     "address" : "How the heck",
#     "place" : "TunnelSchool",
#     "type" : "Pokemon",
#     "imageLink":["https://pbs.twimg.com/profile_images/1250516096907571200/adjxWadZ_400x400.jpg"]
#     },
#     {"id":311,
#     "latitude":"1",
#     "longitude" : "1",
#     "description" : 'noob2xxxxxxx',
#     "address" : "How the heck",
#     "place" : "TunnelSchool",
#     "type" : "Pokemon",
#     "imageLink":["https://pbs.twimg.com/profile_images/1250516096907571200/adjxWadZ_400x400.jpg"]
#     }]

def getMapPoints(request):
    #print(testlst)

    get_marker = list(Marker.objects.all().filter(enable=1,created_user_id=62010893).values(
        "id",
        "latitude",
        "longitude",
        "description",
        "address",
        "place",
        "type",
        "imageLink"
    ))
    
    for rows in get_marker:
        rows['latitude'] = str(rows['latitude'])
        rows['longitude'] = str(rows['longitude'])
        rows['imageLink'] = ast.literal_eval(rows['imageLink'])

    return JsonResponse(get_marker,safe = False)


@api_view(['POST'])
def createLocationQuery(request):
    #print(request.data)
    if request.method == 'POST':

        try:

            global imagenumber
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            place = data_dict["name"]
            detail = data_dict["detail"]
            tag = data_dict["type"]
            file = request.data['image'] # or self.files['image'] in your form
            path = default_storage.save(f'tmp/image.png', ContentFile(file.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            #print(tmp_file)
            
            #print(data_dict)

            latitude = data_dict['latitude']
            longitude = data_dict['longitude']
            nc.put_file(f"KMITLcompanion/image{imagenumber}.png",tmp_file)
            link_info = nc.share_file_with_link(f'KMITLcompanion/image{imagenumber}.png')
            imagenumber = imagenumber+1
            link = link_info.get_link() + "/preview"
            #print(link)

            #testlst.append({"place":name, "id":random.randint(1000,2000), "latitude":latitude , "longitude" : longitude,"description" : "noob2" , "address" : detail , "type" : tag , "imageLink" : [link]})
            #print(latitude," === ",longitude)
            get_User = User.objects.get(student_id=62010893)#***ไว้แก้ทีหลัง
            save_marker = Marker(name=place,
                            place=place,#***ไว้แก้ทีหลัง
                            address=detail,#***ไว้แก้ทีหลัง
                            latitude=latitude,longitude=longitude,
                            description=detail,#***ไว้แก้ทีหลัง
                            type=tag,
                            imageLink=str([link]),
                            created_user=get_User,)
            save_marker.save()

        except Exception as e:
            raise e
            
    return HttpResponse()


@csrf_exempt
def getLocationQuery(request) -> None:
    if request.method == "POST":
        data = request.POST
        latitude = data["latitude"]
        longitude = data["longitude"]

        x = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/{longitude},{latitude}.json?access_token=pk.eyJ1Ijoicnl1aW53MTIzIiwiYSI6ImNsODV5M21odjB0dXAzbm9lZDhnNXVoY2UifQ.IiTAr5ITOUcCVjPjWiRe1w&limit=1")
        data = x.json()

        if (data["features"]):
            feature = data["features"][0]

            response = {
                "place" : feature["text"],
                "address" : feature["place_name"]
            }
        else:
            response = {
                "place" : "The Ocean",
                "address" : " "
            }
        
        return JsonResponse(response,safe=False)