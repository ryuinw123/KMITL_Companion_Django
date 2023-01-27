
import requests
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


#####################


@api_view(['POST'])
def getPinDetailsLocationQuery(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            marker_id = data_dict['id']
            #print(data_dict)


            #/******* Marker Like Data **********/

            get_marker_like_object = MarkerLike.objects.all().filter(markerlike_marker=marker_id)
            isLiked = user_id in list(get_marker_like_object.values_list("markerlike_student",flat=True))
            likeCounting = len(list(get_marker_like_object.values()))

            #/******* Comment Data **********/


            pinDetailsDict = {}
            pinDetailsDict['likeCounting'] = likeCounting
            pinDetailsDict['isLiked'] = isLiked
            print("Pin Details = ",pinDetailsDict)

            return JsonResponse(pinDetailsDict,safe = False)

        except Exception as e:
            raise e
    
    return HttpResponse()

@api_view(['POST'])
def likeLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            marker_id = data_dict['id']
            print("likeLocationQuery",marker_id)

            get_User = User.objects.get(student_id=user_id)
            get_Marker = Marker.objects.get(id=int(marker_id))
            saveLike = MarkerLike.objects.create(markerlike_marker=get_Marker,markerlike_student=get_User)

        except Exception as e:
            raise e
            
    return HttpResponse()


@api_view(['POST'])
def dislikeLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            marker_id = data_dict['id']
            print("dislikeLocationQuery")

            get_User = User.objects.get(student_id=user_id)
            get_Marker = Marker.objects.get(id=int(marker_id))
            get_marker_like_object = MarkerLike.objects.all().filter(markerlike_marker=marker_id,markerlike_student=user_id)
            get_marker_like_object.delete()


        except Exception as e:
            raise e
            
    return HttpResponse()