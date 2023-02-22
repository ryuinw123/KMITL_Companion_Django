from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
import os
import json

#models
from ....models import *

#utils
from ....utils import *

#<QueryDict: {'id': ['18'], 'token': ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMDEwODkzIiwiZW1haWwiOiI2MjAxMDg5M0BrbWl0bC5hYy50aCIsImV4cCI6MzU2MzAxMTMyNCwiaWF0IjoxNjcwODUxMzI0fQ.dxsOyXLIy-zGTcHXDBGwmJJz63nNxC9OspY41jtNWwQ']}>

@api_view(['POST'])
def getEventDetailsLocationQuery(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            event_id = data_dict['id']

            

            #/******** check My Marker ***********/
            get_event_object = Event.objects.all().filter(event_id=event_id)
            isMyPin =  list(get_event_object.filter(student=user_id).values()) != []
            created_user_name_id = list(get_event_object.values_list("student",flat=True))[0]
            if (created_user_name_id != user_id) :
                created_user = User.objects.filter(student_id=created_user_name_id)
                created_user_name = (list(created_user.values_list("firstname",flat=True))[0]) + " " +(list(created_user.values_list("lastname",flat=True))[0])
            else:
                created_user_name = "ฉัน"
            #/******* Event Like Data **********/

            get_event_like_object = EventLike.objects.all().filter(event_like_event=event_id)
            isEventLiked = user_id in list(get_event_like_object.values_list("event_like_student",flat=True))
            likeCounting = len(list(get_event_like_object.values()))

            #/******* Event Bookmark Data *************/
            get_event_bookmark_object = EventBookmark.objects.all().filter(event_bookmark_student=user_id,event_bookmark_event=event_id)
            isEventBookmarked = user_id in list(get_event_bookmark_object.values_list("event_bookmark_student",flat=True))


            returnDict = {
                "eventLikeCounting" : likeCounting,
                "isEventLiked" : isEventLiked,
                "isEventBookmarked" : isEventBookmarked,
                "isMyPin" : isMyPin,
                "createdUserName" : created_user_name
            }

            #print("getEventDetailsLocationQuery =====> ",returnDict)

            return JsonResponse(returnDict,safe = False)

        except Exception as e:
            raise e
            
    return HttpResponse()  

@api_view(['POST'])
def getAllEventBookMarker(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])

            get_event_bookmark_object = EventBookmark.objects.all().filter(event_bookmark_student=user_id)
            bookmarkList = list(get_event_bookmark_object.values_list("event_bookmark_event",flat=True))

            print("getAllEventBookMarker =>>>>>>>>",bookmarkList)

            return JsonResponse(bookmarkList,safe = False)

        except Exception as e:
            raise e
            
    return HttpResponse()  


#changeEventLikeLocationQuery =>  <QueryDict: {'eventId': ['6'], 'isLiked': ['true'], 'token': ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMDEwODkzIiwiZW1haWwiOiI2MjAxMDg5M0BrbWl0bC5hYy50aCIsImV4cCI6MzU2MzAxMTMyNCwiaWF0IjoxNjcwODUxMzI0fQ.dxsOyXLIy-zGTcHXDBGwmJJz63nNxC9OspY41jtNWwQ']}>

@api_view(['POST'])
def changeEventLikeLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            event_id = data_dict['eventId']
            is_liked = data_dict['isLiked']
            print("changeEventLikeLocationQuery => ",data_dict)

            if is_liked == "true":
                get_User = User.objects.get(student_id=user_id)
                get_Event = Event.objects.get(event_id=int(event_id))
                saveLike = EventLike.objects.create(event_like_event=get_Event,event_like_student=get_User,createtime=datetime.now())
            elif is_liked == "false":
                get_event_like_object = EventLike.objects.all().filter(event_like_event=event_id,event_like_student=user_id)
                get_event_like_object.delete()

        except Exception as e:
            raise e
            
    return HttpResponse()   

#changeEventBookmarkLocationQuery =>  <QueryDict: {'eventId': ['6'], 'isMark': ['true'], 'token': ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMDEwODkzIiwiZW1haWwiOiI2MjAxMDg5M0BrbWl0bC5hYy50aCIsImV4cCI6MzU2MzAxMTMyNCwiaWF0IjoxNjcwODUxMzI0fQ.dxsOyXLIy-zGTcHXDBGwmJJz63nNxC9OspY41jtNWwQ']}>

@api_view(['POST'])
def changeEventBookmarkLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            event_id = data_dict['eventId']
            is_mark = data_dict['isMark']
            print("changeEventBookmarkLocationQuery => ",data_dict)

            if is_mark == "true":
                get_User = User.objects.get(student_id=user_id)
                get_Event = Event.objects.get(event_id=int(event_id))
                saveLike = EventBookmark.objects.create(event_bookmark_event=get_Event,event_bookmark_student=get_User,createtime=datetime.now())
                print("bookmark true")
            elif is_mark == "false":
                get_event_like_object = EventBookmark.objects.all().filter(event_bookmark_event=event_id,event_bookmark_student=user_id)
                get_event_like_object.delete()
                print("bookmark false")

        except Exception as e:
            raise e
            
    return HttpResponse()   

@api_view(['POST'])
def deleteEventLocationQuery(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            event_id = data_dict['id']

            get_Marker = Event.objects.get(event_id=int(event_id))
            get_Marker.enable = 0
            get_Marker.save()
        
            print("******************************** deleteEventLocationQuery *****************************")
        except Exception as e:
            raise e
            
    return HttpResponse()