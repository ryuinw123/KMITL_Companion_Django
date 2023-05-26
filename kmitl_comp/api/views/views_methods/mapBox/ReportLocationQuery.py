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


@api_view(['POST'])
def reportMarkerLocationQuery(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            id = data_dict['id']
            reason = data_dict['reason']
            details = data_dict['details']

            get_Marker = Marker.objects.get(id=int(id))
            get_User = User.objects.get(student_id=user_id)

            report_marker = ReportMarker(id=get_Marker,reason=reason,details=details,created_user=get_User,created_time=datetime.now())
            report_marker.save()
        
            #print("******************************** reportMarkerLocationQuery *****************************",data_dict)
        except Exception as e:
            raise e
            
    return HttpResponse()


@api_view(['POST'])
def reportEventLocationQuery(request):
    if request.method == 'POST':
        try:
            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            id = data_dict['id']
            reason = data_dict['reason']
            details = data_dict['details']

            get_Event = Event.objects.get(event_id=int(id))
            get_User = User.objects.get(student_id=user_id)

            report_event = ReportEvent(event=get_Event,reason=reason,details=details,created_user=get_User,created_time=datetime.now())
            report_event.save()
            #print("******************************** reportEventLocationQuery *****************************",data_dict)
        except Exception as e:
            raise e
            
    return HttpResponse()