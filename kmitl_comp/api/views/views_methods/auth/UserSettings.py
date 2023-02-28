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


@api_view(['POST'])
def settingsGetUserData(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])

            get_user_object = User.objects.get(student_id=user_id)

            returnDict = {
                "username" : get_user_object.firstname + " " + get_user_object.lastname,
                "faculty" : get_user_object.faculty,
                "email" : get_user_object.email,
                "department" : get_user_object.department,
                "year" : get_user_object.year
            }
        

            return JsonResponse(returnDict,safe=False)
            print("******************************** settingsGetUserData *****************************",get_user_object)
        except Exception as e:
            raise e
            
    return HttpResponse()


@api_view(['POST'])
def settingsEditUpdateUserData(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])

            name = data_dict['username']
            firstname = name.split(" ")[0]
            lastname = name.split(" ")[1]
            faculty = data_dict['faculty']
            department = data_dict['department']
            year = data_dict['year']

            get_user_object = User.objects.get(student_id=user_id)
            get_user_object.firstname = firstname
            get_user_object.lastname = lastname
            get_user_object.faculty = faculty
            get_user_object.department = department
            get_user_object.year = year
            get_user_object.save()

            print("******************************** settingsEditUpdateUserData *****************************",
                   get_user_object.faculty)
        except Exception as e:
            raise e
            
    return HttpResponse()