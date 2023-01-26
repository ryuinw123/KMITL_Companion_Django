
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
def getLikeLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            #name = data_dict["name"]
            print("location like query successss")

        except Exception as e:
            raise e
            
    return HttpResponse()

@api_view(['POST'])
def likeLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            #name = data_dict["name"]


        except Exception as e:
            raise e
            
    return HttpResponse()


@api_view(['POST'])
def dislikeLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            #name = data_dict["name"]


        except Exception as e:
            raise e
            
    return HttpResponse()