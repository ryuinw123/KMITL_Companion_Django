from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from .views import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #Test Methods
    #testapi
    path('testtoken', views.testMethods.testMethod.testToken),
    path('checktoken', views.testMethods.testMethod.checkToken),

    #Auth Methods
    #UserApi
    path('login', views.auth.Login.userLogin),
    path('postuserdata', views.auth.Login.postUserData),

    #MapBox Methods
    #locationAPI
    path('getlocationquery',views.mapBox.locationQuery.getLocationQuery),

    #createLocationQuery
    path('createlocationquery',views.mapBox.locationQuery.createLocationQuery),#

    #createPublicLocationQuery
    path('createpubliclocationquery',views.mapBox.locationQuery.createPublicLocationQuery),#


    #getMapPoints
    path('getmappoints', views.mapBox.locationQuery.getMapPoints),
]
