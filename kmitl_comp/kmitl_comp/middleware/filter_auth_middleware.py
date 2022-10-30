from django.core.exceptions import BadRequest
from django.forms import ValidationError
from django.http import HttpResponseBadRequest

# #oauth
# from google.oauth2 import id_token
# from google.auth.transport import requests

import requests as req

from api.models import *

import regex as re

class FilterAuthMiddleware(object):

    def __init__(self, next_layer=None):
        """We allow next_layer to be None because old-style middlewares
        won't accept any argument.
        """
        self.get_response = next_layer

    def process_request(self, request):#check refresh token
        """Let's handle old-style request processing here, as usual."""
        # check token auth with google

        if request.method == 'POST':
            data_dict = request.POST
            print("check auth ! ! ! ....")

            if 'authCode' in data_dict:
                return
            
            refresh_token = data_dict['token']
            refresh_token = re.sub('["\']', '', refresh_token)

            print("refresh_token",refresh_token)

            # data = {
            #     'client_id': GoogleAuthConsoleData().client_id,
            #     'client_secret': GoogleAuthConsoleData().client_secret,
            #     'grant_type': 'refresh_token',
            #     'refresh_token' : refresh_token
            # }
            # response = req.post("https://oauth2.googleapis.com/token", data=data)
            # if not response.ok:
            #     raise ValidationError('Failed to obtain access token from Google with refresh token.')
            # access_token = response.json()
            # return access_token
            return

        # if request.method == 'POST':
        #     data_dict = request.POST
        #     print("check auth ! ! ! ....")

        #     try:
        #         authCode = data_dict['authCode']
        #         if authCode != "":
        #             return
        #     except:

        #         token = data_dict['token']
        #         token = re.sub('["\']', '', token)
            
        #         request = requests.Request()

        #         try:
        #             id_info = id_token.verify_oauth2_token(token, request, GoogleAuthConsoleData().client_id)
                    

        #             auth_userdata = id_info
        #             hd = auth_userdata['email'].split('@')[-1]

        #             if hd != "kmitl.ac.th":
        #                 print("This not kmitl account")
        #                 raise BadRequest('Invalid request')

        #             print("Token : ",token,"\n")
        #             AuthDataStore().name = auth_userdata['name']
        #             AuthDataStore().email = auth_userdata['email']
        #             AuthDataStore().given_name = auth_userdata['given_name']
        #             AuthDataStore().family_name = auth_userdata['family_name']
        #             AuthDataStore().hd = hd

        #             print("/*************************/\n","Validation successfully !!\n",auth_userdata,"\n/*************************/","\n\n")

        #         except Exception as e:
        #             print("/*************************/\n","Validation failed !!\n",e,"\n/*************************/","\n\n")
        #             raise BadRequest('You not Login, Invalid request')



    def process_response(self, request, response):
        """Let's handle old-style response processing here, as usual."""
        # Do something with response, possibly using request.
        return response

    def __call__(self, request):
        """Handle new-style middleware here."""
        response = self.process_request(request)
        if response is None:
        # If process_request returned None, we must call the next middleware or
        # the view. Note that here, we are sure that self.get_response is not
        # None because this method is executed only in new-style middlewares.
            response = self.get_response(request)
        response = self.process_response(request, response)
        return response