
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
import os
import json
import copy
import secrets
import string
import re as re
from django.db.models import Q
import math
import ast
#models
from ....models import *

#utils
from ....utils import *


#####################
def filter_marker_list(lst, field, pattern):
    regex = re.compile(pattern,re.IGNORECASE)

    resultList = []
    for item in lst:
        match_found = False
        for field_item in field:
            if regex.search(item.get(field_item)):
                match_found = True
                break
        if match_found:
            resultList.append(item)
   
    #sorted_list = sorted(resultList, key=lambda x: sum(1 for f in field if regex.search(x.get(f))))
    return resultList


def calDistanceBetween(resultList,current_lat,current_long):

    for item in resultList:
        if item.get('latitude') == None:
            area =  ast.literal_eval(item.get('polygon'))
            center = calculate_center(area)
            lat = center[1]
            long = center[0]
            distance = distanceBe(lat,long,current_lat,current_long)#math.sqrt((lat - current_lat)**2 + (long - current_long)**2)
            item['distance'] = distance

        else:
            lat = float(item.get('latitude'))
            long = float(item.get('longitude'))
            distance = distanceBe(lat,long,current_lat,current_long)#math.sqrt((lat - current_lat)**2 + (long - current_long)**2)
            item['distance'] = distance

    sorted_list = sorted(resultList, key=lambda k: k['distance'])

    return sorted_list

def distanceBe(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the earth in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def calculate_center(coords):
    n = len(coords)
    x = sum(p[0] for p in coords) / n
    y = sum(p[1] for p in coords) / n
    return [round(x, 6), round(y, 6)]





@api_view(['POST'])
def getSearchDetailsQuery(request):
    if request.method == 'POST':
        try:
            
            data = request.POST
            newdata = dataRefacter(data)
            user_id = returnUserIdFromToken(newdata['token'])
            typeList = data.getlist('typeList')
            typeList = [int(x) for x in typeList]
            typeList = returnTypeCodeToName(typeList)
            text = newdata['text']
            
            latitude = newdata['lat']
            longitude = newdata['long']

            #print("hello world this is search =>>>>>>>>>>>>>>>>>>>>",newdata)
            get_User = User.objects.get(student_id=user_id)

            #get normal marker
            get_public_marker_obj = PermissionMarker.objects.all().values_list("pm_maker",flat=True)
            get_marker_obj = Marker.objects.all().filter(enable=1,
                                                        created_user_id=user_id,
                                                        type__in=typeList,
                                                        ).union(
                            Marker.objects.all().filter(enable=1,
                                                        id__in=list(get_public_marker_obj),
                                                        type__in=typeList,                                        
                                                        ))
            
            
            get_event_object = Event.objects.none()
            now = datetime.now()
            #ถ้ามี event ใน type
            if (969 in typeList):
                get_event_object = Event.objects.all().filter(enable=1,endtime__gte=now)


            #ถ้า มี bookmark ใน type
            if (100 in typeList):
                typeList.remove(100)
                get_bookmark_object = Bookmark.objects.all().filter(bookmark_student=user_id)
                bookmarkList = list(get_bookmark_object.values_list("bookmark_marker",flat=True))
                get_marker_obj = get_marker_obj.union(Marker.objects.all().filter(enable=1,
                                                                                    id__in=bookmarkList,
                                                                                    ))
                
                get_event_bookmark_object = EventBookmark.objects.all().filter(event_bookmark_student=user_id)
                eventList = list(get_event_bookmark_object.values_list("event_bookmark_event",flat=True))
                get_event_object = get_event_object.union(Event.objects.all().filter(enable=1,endtime__gte=now,event_id__in=eventList))


            all_marker_list = list(get_marker_obj.values())
            all_event_list = list(get_event_object.values()) if get_event_object != None else []

            

            #filtered_list = filter_list(all_marker_list, 'name', (r'^([\w{}])*').format(t))
            filtered = all_marker_list
            filtered_event = all_event_list
            if (text != ""):
                filtered = filter_marker_list(all_marker_list, ['name','place','address'], text,)
                filtered_event = filter_marker_list(all_event_list,['eventname','description'], text)

            all_filterd_list = calDistanceBetween(filtered + filtered_event,float(latitude),float(longitude))
    
            #for marker
            searchResultList = []

            for data in all_filterd_list:
                searchResultList.append(
                    {
                        "id" : data.get('event_id', data.get('id', None)),
                        "name" : data.get('eventname', data.get('name', None)),
                        "place" :  data.get('place'," "),
                        "address" : data.get('address'," "),
                        "pic" : 0,
                        "code" : returnNameToTypeCode(data.get('type',969)),
                        "distance" : round(data.get('distance'),1)
                    }
                )
            
            #print("result of search =>>>>>>>>>>>>>>>>>>>>>>>>: ",searchResultList)

            return JsonResponse(searchResultList,safe = False)
        except Exception as e:
            raise e
    
    return HttpResponse()