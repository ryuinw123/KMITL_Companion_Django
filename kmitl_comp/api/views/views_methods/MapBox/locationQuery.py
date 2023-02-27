
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

def getEventLocations(request):

    token = request.GET.get('token')

    now = datetime.now()

    get_event_obj = Event.objects.all().filter(enable=1,endtime__gte=now)
    event_list = list(get_event_obj.values("event_id","eventname","description","starttime","endtime","polygon"))

    get_image_event = list(ImageEvent.objects.filter(event__in=list(get_event_obj.values_list('event_id',flat=True))).values("event","link"))

    returnListDict = []

    for event in event_list:
        event_polygon = ast.literal_eval(event['polygon'])
        event_polygon_list = [{'coordinates': [point[0], point[1]], 'type': 'Point'} for point in event_polygon]
        returnListDict.append(
            {
                'name': event['eventname'],
                'description': event['description'],
                'id': event['event_id'],
                'startTime': event['starttime'].strftime("%d/%m/%Y %H:%M"),#.strftime("%d/%m/%Y %H:%M")
                'endTime': event['endtime'].strftime("%d/%m/%Y %H:%M"),#.strftime("%d/%m/%Y %H:%M")
                'area': event_polygon_list,
                'imageLink': [sub['link'] for sub in get_image_event if sub['event'] == event['event_id']],
            }
        )

    #print("get_event : ",returnListDict)
    return JsonResponse(returnListDict,safe = False)


#{'name': ['""'], 'description': ['""'], 'status': ['"private"'], 'point': ['{"coordinates":[100.43714217283895,13.563551298705264],"type":"Point"}', '{"coordinates":[100.61192039687631,13.565510398593304],"type":"Point"}', '{"coordinates":[100.60792085751842,13.791609649391248],"type":"Point"}', '{"coordinates":[100.43915017202153,13.781890881272716],"type":"Point"}'], 'token': ['"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMDEwODkzIiwiZW1haWwiOiI2MjAxMDg5M0BrbWl0bC5hYy50aCIsImV4cCI6MzU2MzAxMTMyNCwiaWF0IjoxNjcwODUxMzI0fQ.dxsOyXLIy-zGTcHXDBGwmJJz63nNxC9OspY41jtNWwQ"']}

# def post(self, request, *args, **kwargs):
        
#         file = request.FILES['file']
#         marker_id = request.POST.get('marker_id')
        
#         # Save the image to default storage
#         path = default_storage.save(f'tmp/image.png', ContentFile(file.read()))
#         tmp_file = os.path.join(settings.MEDIA_ROOT, path)

#         index = Image.objects.latest('image_id').image_id + 1

#         nc.put_file(f"KMITLcompanion/image{index}.png", tmp_file)
#         link_info = nc.share_file_with_link(f'KMITLcompanion/image{index}.png')
        
#         # Save the image data to the database
#         image = Image.objects.create(marker_id=marker_id, link=f'{link_info.get_link()}/preview')
#         serializer = self.get_serializer(image)

#         os.remove(settings.MEDIA_ROOT + tmp_file)

#         return Response(serializer.data)

@api_view(['POST'])
def createEventQuery(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            point_dict = request.data.getlist('point')
            user_id = returnUserIdFromToken(data_dict['token'])
            event_name = data_dict['name']
            event_des = data_dict['description']
            event_start = data_dict['startTime']
            event_end = data_dict['endTime']
            file = request.data.getlist('image')
            link = []

            if file != []:
                for _index,file_ in enumerate(file):
                    path = default_storage.save(f'tmp/image.png', ContentFile(file_.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)

                    index = ImageEvent.objects.latest('image_id').image_id + 1 + _index

                    nc.put_file(f"KMITLcompanion/image{index}.png", tmp_file)
                    link_info = nc.share_file_with_link(f'KMITLcompanion/image{index}.png')

                    ##imagenumber = imagenumber+1

                    link.append(link_info.get_link() + "/preview")
                    #/*** remove tmp file ****/
                    os.remove(settings.MEDIA_ROOT + tmp_file)


            # convert each string in the    list to a dictionary
            dict_list = [json.loads(coord) for coord in point_dict]

            # extract the coordinates from each dictionary and convert to a list
            polygon = [[round(coord, 8) for coord in item['coordinates']] for item in dict_list]


            get_User = User.objects.get(student_id=user_id)
            save_event = Event(
                            eventname=event_name,
                            description=event_des,
                            starttime=datetime.strptime(event_start, '%d/%m/%Y %H:%M'),
                            endtime=datetime.strptime(event_end, '%d/%m/%Y %H:%M'),
                            polygon=str(polygon),
                            student=get_User,
                            createtime=datetime.now(),
                            enable=1,
                            )
            save_event.save()

            if link != []:
                for _link in link:
                    save_image = ImageEvent(event=save_event,link=_link)
                    save_image.save()

            print("eventdictxxxxxxxxxxxxxxxxxxxxxxxxxxxx",data_dict)
            

        except Exception as e:
            raise e
            
    return HttpResponse()

def getMapPoints(request):
    #print(testlst)
    token = request.GET.get('token')
    #print("token : ",token)


    get_public_marker_obj = PermissionMarker.objects.all().values_list("pm_maker",flat=True)

    get_marker_obj = Marker.objects.all().filter(enable=1,created_user_id=returnUserIdFromToken(token)).union(
                     Marker.objects.all().filter(enable=1,id__in=list(get_public_marker_obj)))
    
    get_marker = list(get_marker_obj.values(
                    "id",
                    "name",
                    "latitude",
                    "longitude",
                    "description",
                    "address",
                    "place",
                    "type",
                 ))
    get_image_marker = list(Image.objects.filter(marker__in=list(get_marker_obj.values_list('id',flat=True))).values("marker","link"))
    
    for rows in get_marker:
        rows['latitude'] = str(rows['latitude'])
        rows['longitude'] = str(rows['longitude'])
        rows.update({"imageLink" : [sub['link'] for sub in get_image_marker if sub['marker'] == rows['id']]})

    #print("get_marker : ",get_marker,"\n ",type(get_marker))
    return JsonResponse(get_marker,safe = False)


@api_view(['POST'])
def createLocationQuery(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            name = data_dict["name"]
            place = data_dict["place"]
            address = data_dict["address"]
            description = data_dict["description"]
            type = data_dict["type"]
            latitude = data_dict['latitude']
            longitude = data_dict['longitude']
            file = request.data.getlist('image')

            link = []

            if file != []:
                for _index,file_ in enumerate(file):
                    path = default_storage.save(f'tmp/image.png', ContentFile(file_.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)

                    index = Image.objects.latest('image_id').image_id + 1 + _index

                    nc.put_file(f"KMITLcompanion/image{index}.png", tmp_file)
                    link_info = nc.share_file_with_link(f'KMITLcompanion/image{index}.png')


                    link.append(link_info.get_link() + "/preview")
                    #/*** remove tmp file ****/
                    os.remove(settings.MEDIA_ROOT + tmp_file)

            get_User = User.objects.get(student_id=returnUserIdFromToken(data_dict['token']))
            save_marker = Marker(name=name,
                            place=place,
                            address=address,
                            latitude=latitude,longitude=longitude,
                            description=description,
                            type=type,
                            created_user=get_User,)
            save_marker.save()

            if link != []:
                for _link in link:
                    save_image = Image(marker=save_marker,link=_link)
                    save_image.save()

        except Exception as e:
            raise e
            
    return HttpResponse()

@api_view(['POST'])
def createPublicLocationQuery(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            name = data_dict["name"]
            place = data_dict["place"]
            address = data_dict["address"]
            description = data_dict["description"]
            type = data_dict["type"]
            latitude = data_dict['latitude']
            longitude = data_dict['longitude']
            file = request.data.getlist('image')

            link = []

            if file != []:
                for _index,file_ in enumerate(file):
                    path = default_storage.save(f'tmp/image.png', ContentFile(file_.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)

                    index = Image.objects.latest('image_id').image_id + 1 + _index

                    nc.put_file(f"KMITLcompanion/image{index}.png", tmp_file)
                    link_info = nc.share_file_with_link(f'KMITLcompanion/image{index}.png')

                    link.append(link_info.get_link() + "/preview")
                    #/*** remove tmp file ****/
                    os.remove(settings.MEDIA_ROOT + tmp_file)

            get_User = User.objects.get(student_id=returnUserIdFromToken(data_dict['token']))
            save_marker = Marker(name=name,
                            place=place,
                            address=address,
                            latitude=latitude,longitude=longitude,
                            description=description,
                            type=type,
                            created_user=get_User,)
            save_marker.save()

            if link != []:
                for _link in link:
                    save_image = Image(marker=save_marker,link=_link)
                    save_image.save()

            #/*** crete public permission ****/
            save_permission = Permission(permission_student=get_User)
            save_permission.save()

            save_marker_permission = PermissionMarker(pm_permission=save_permission,pm_maker=save_marker)
            save_marker_permission.save()

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