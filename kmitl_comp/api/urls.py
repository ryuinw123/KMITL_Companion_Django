from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from .views import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #UserApi
    path('login', views.Auth.Login.userLogin),
    path('postuserdata', views.Auth.Login.postUserData),

    #testapi
    path('helloworld', views.TestMethods.testMethod.helloWorld),
    path('testtoken', views.TestMethods.testMethod.testToken),
    path('checktoken', views.TestMethods.testMethod.checkToken),
    path('testpost', views.TestMethods.testMethod.testpost),

    #locationAPI
     path('getlocationquery',views.MapBox.locationQuery.getLocationQuery),

    #path('eiei',views.Auth.views_login.testmethod),
    #path('eiei2',views.testmethod2),

]
