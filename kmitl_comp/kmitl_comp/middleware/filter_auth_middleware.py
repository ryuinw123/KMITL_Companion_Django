from django.core.exceptions import BadRequest
from django.http import HttpResponseBadRequest

#oauth
from google.oauth2 import id_token
from google.auth.transport import requests


class FilterAuthMiddleware(object):

    def __init__(self, next_layer=None):
        """We allow next_layer to be None because old-style middlewares
        won't accept any argument.
        """
        self.CLIENT_ID = "563509002084-b7m05boiaqs5mo0thi4ka59noiakeus2.apps.googleusercontent.com"
        self.get_response = next_layer

    def process_request(self, request):
        """Let's handle old-style request processing here, as usual."""
        # check token auth with google

        if request.method == 'POST':
            data_dict = request.POST
            print("check auth ! ! ! ....")
            #print(data_dict)

            token = data_dict['token']
            token = token[1:-1]

            print("Token : ",token,"\n")
            
            request = requests.Request()

            try:
                id_info = id_token.verify_oauth2_token(token, request, self.CLIENT_ID)

                auth_userdata = id_info

                print("/*************************/\n","Auth Success\n",auth_userdata,"\n/*************************/","\n\n")

            except Exception as e:
                print("/*************************/\n",e,"\n/*************************/","\n\n")
                raise BadRequest('You not Login, Invalid request')



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