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

    #getpindetailslocationquery
    path('getpindetailslocationquery', views.mapBox.MarkerDetailsQuery.getPinDetailsLocationQuery),

    #likelocationquery
    path('likelocationquery', views.mapBox.MarkerDetailsQuery.likeLocationQuery),

    #dislikelocationquery
    path('dislikelocationquery', views.mapBox.MarkerDetailsQuery.dislikeLocationQuery),

    #addcommentmarkerlocationquery
    path('addcommentmarkerlocationquery', views.mapBox.MarkerDetailsQuery.addCommentMarkerLocationQuery),

    #editcommentmarkerlocationquery
    path('editcommentmarkerlocationquery', views.mapBox.MarkerDetailsQuery.editCommentMarkerLocationQuery),

    #deletecommentmarkerlocationquery
    path('deletecommentmarkerlocationquery', views.mapBox.MarkerDetailsQuery.deleteCommentMarkerLocationQuery),

    #likedislikecommentmarkerlocationquery
    path('likedislikecommentmarkerlocationquery', views.mapBox.MarkerDetailsQuery.likeDislikeCommentMarkerLocationQuery),
]
