from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #UserApi
    path('login', views.userLogin),
    path('postuserdata', views.postUserData),


    #testapi
    path('helloworld', views.helloWorld),
    path('testtoken', views.testToken),
    path('checktoken', views.checkToken),
    path('testpost',views.testpost)
]
