
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
#models
from ....models import *

#utils
from ....utils import *


#####################
def filter_list(lst, field, pattern):
    regex = re.compile(pattern,re.IGNORECASE)
    resultList = [item for item in lst if (regex.search(item.get(field[0])) 
                    or regex.search(item.get(field[1])) 
                    or regex.search(item.get(field[2])))]

    sorted_list = sorted(resultList, key=lambda x: sum(1 for f in field if regex.search(x.get(f))))

    return sorted_list

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

            print("hello world this is search",text)
            get_User = User.objects.get(student_id=user_id)


            pattern = re.compile("r^([A-z])", re.IGNORECASE)
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

            if (100 in typeList):
                typeList.remove(100)
                get_bookmark_object = Bookmark.objects.all().filter(bookmark_student=user_id)
                bookmarkList = list(get_bookmark_object.values_list("bookmark_marker",flat=True))
                get_marker_obj = get_marker_obj.union(Marker.objects.all().filter(enable=1,
                                                                                    id__in=bookmarkList,
                                                                                    ))
            #code bookmark here
            #test_marker_obj = Marker.objects.filter(name__iregex=r'^([{}]||{})+'.format(t,t)).values("name")

            all_marker_list = list(get_marker_obj.values())
            #filtered_list = filter_list(all_marker_list, 'name', (r'^([\w{}])*').format(t))
            filtered = all_marker_list
            if (text != ""):
                filtered = filter_list(all_marker_list, ['name','place','address'], text)
            # filtered_place = filter_list(all_marker_list, 'place', t)
            # filtered_address = filter_list(all_marker_list, 'address', t)
            # filtered_list = filtered_name.union(filtered_place).union(filtered_address)
            
            #print("ressult lit search ",list(get_marker_obj.values_list('id',flat=True)))

            #print("ressult lit search ",filtered_list)
            #search here

            searchResultList = []
            for d in filtered:

                searchResultList.append(
                    {
                        "id" : d['id'],
                        "name" : d['name'],
                        "place" : d['place'],
                        "address" : d['address'],
                        "pic" : 0,
                        "code" : returnNameToTypeCode(d['type']),
                    }
                )
            
            print("result of search : ",searchResultList)

            return JsonResponse(searchResultList,safe = False)
        except Exception as e:
            raise e
    
    return HttpResponse()