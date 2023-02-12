
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

            #/******* Bookmark Data *************/
            get_bookmark_object = Bookmark.objects.all().filter(bookmark_student=user_id,bookmark_marker=marker_id)
            isBookmarked = user_id in list(get_bookmark_object.values_list("bookmark_student",flat=True))
            print("is bookemarked ,,,,,,,,,,,,,,,,,,, ",isBookmarked)

            #/******* Comment Data **********/
            get_comment_object = Comment.objects.all().filter(comment_marker=marker_id)
            id_list = list(get_comment_object.values_list("comment_id",flat=True))
            get_comment_like_object = CommentLike.objects.all().filter(cl_comment__in = id_list)
            commentLikeCounting = get_comment_like_object.filter(islike=1)
            commentDisLikeCounting = get_comment_like_object.filter(islike=0)

            get_comment_list = list(get_comment_object.all().order_by('-createtime')
                                    .filter(comment_student = user_id).values("comment_id","content","comment_student","createtime")) + list(
                                    get_comment_object.order_by('-createtime').exclude(comment_student = user_id)
                                    .values("comment_id","content","comment_student","createtime"))
           
            
            #print("comment like ",commentLikeCounting)
            #print("comment  ",get_comment_list)


            #/************** make comment data **************/

            commentList = []
            userQuerySet = set()
            userQuery = {}

            for i in range( len(get_comment_list) ) :
                di = {}
                if (get_comment_list[i]["comment_student"] not in userQuerySet):
                    userQuery[get_comment_list[i]["comment_student"]] = User.objects.get(student_id=get_comment_list[i]["comment_student"])
                    userQuerySet.add(get_comment_list[i]["comment_student"])

                di["id"] = get_comment_list[i]["comment_id"]
                di["date"] = get_comment_list[i]["createtime"].strftime("%d/%m/%Y %H:%M")
                di["author"] = userQuery.get(get_comment_list[i]["comment_student"]).firstname +" "+ userQuery.get(get_comment_list[i]["comment_student"]).lastname
                di["message"] = get_comment_list[i]["content"]
                di["like"] = len(list(commentLikeCounting.filter(cl_comment=get_comment_list[i]["comment_id"]).values()))
                di["dislike"] = len(list(commentDisLikeCounting.filter(cl_comment=get_comment_list[i]["comment_id"]).values()))
                di["isLikedComment"] = list(commentLikeCounting.filter(cl_comment=get_comment_list[i]["comment_id"],cl_student = user_id).values()) != []
                di["isDisLikedComment"] = list(commentDisLikeCounting.filter(cl_comment=get_comment_list[i]["comment_id"],cl_student = user_id).values()) != []
                di["myComment"] = get_comment_list[i]["comment_student"] == user_id
                commentList.append(di)
                #print(di)

            # pinDetailsDict['comment'] = [
            #     {
            #         "id":"",
            #         "date":"",
            #         "author":"",
            #         "message":"",
            #         "like":"",
            #         "dislike":"",
            #         "isLikedComment":"",
            #         "isDisLikedComment":"",
            #         "myComment":""
            #     }
            # ]



            pinDetailsDict = {}
            pinDetailsDict['likeCounting'] = likeCounting
            pinDetailsDict['isLiked'] = isLiked
            pinDetailsDict['comment'] = commentList
            pinDetailsDict['isBookmarked'] = isBookmarked

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
            print("likeLocationQuery")

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

@api_view(['POST'])
def addCommentMarkerLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            marker_id = data_dict['id']
            comment = data_dict['message']

            get_User = User.objects.get(student_id=user_id)
            get_Marker = Marker.objects.get(id=int(marker_id))
            saveComment = Comment(comment_marker=get_Marker,content = comment,comment_student=get_User,createtime=datetime.now())
            saveComment.save()
            
            returnDict = {"commentId":saveComment.comment_id,"author":get_User.firstname + " " + get_User.lastname}
            print("add Comment pin at ",returnDict)
            return JsonResponse(returnDict,safe = False)
        except Exception as e:
            raise e
    return HttpResponse()


@api_view(['POST'])
def addCommentMarkerLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            marker_id = data_dict['id']
            comment = data_dict['message']

            get_User = User.objects.get(student_id=user_id)
            get_Marker = Marker.objects.get(id=int(marker_id))
            saveComment = Comment(comment_marker=get_Marker,content = comment,comment_student=get_User,createtime=datetime.now())
            saveComment.save()
            
            returnDict = {"commentId":saveComment.comment_id,"author":get_User.firstname + " " + get_User.lastname}
            print("add Comment pin at ",returnDict)
            return JsonResponse(returnDict,safe = False)
        except Exception as e:
            raise e
    return HttpResponse()


@api_view(['POST'])
def editCommentMarkerLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            marker_id = data_dict['id']
            comment = data_dict['newmessage']

            Comment.objects.filter(comment_id=marker_id).update(comment_id=marker_id,content=comment,createtime=datetime.now())
            
            print("add Comment pin at ",data_dict)
            # return JsonResponse(returnDict,safe = False)
        except Exception as e:
            raise e
    return HttpResponse()

@api_view(['POST'])
def deleteCommentMarkerLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            comment_id = data_dict['id']
            

            delCommentLike = CommentLike.objects.filter(cl_comment=comment_id).delete()
            delComment = Comment.objects.filter(comment_id=comment_id).delete()

            print("delete Comment pin at ",delComment)

        except Exception as e:
            raise e
    return HttpResponse()

@api_view(['POST'])
def likeDislikeCommentMarkerLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            comment_id = data_dict['id']
            is_like = int(data_dict['isLikedComment'])
            is_dislike = int(data_dict['isDisLikedComment'])
            print("likedislike Comment pin at ")

            get_comment = Comment.objects.get(comment_id=comment_id)
            get_User = User.objects.get(student_id=user_id)

            get_commentlike = CommentLike.objects.filter(cl_comment=get_comment,cl_student=get_User)
            if (is_like == 0 and is_dislike == 0):
                print("delete")
                get_commentlike.delete()
            else:

                if (list(get_commentlike.values()) == []):
                    CommentLike.objects.create(cl_comment=get_comment,cl_student=get_User,islike=is_like,createtime=datetime.now())
                else:
                    get_commentlike.update(islike=is_like,createtime=datetime.now())         

        except Exception as e:
            raise e
    return HttpResponse()


@api_view(['POST'])
def getAllBookmakerLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])

            #get_User = User.objects.get(student_id=user_id)
            get_bookmark_object = Bookmark.objects.all().filter(bookmark_student=user_id)
            bookmarkList = list(get_bookmark_object.values_list("bookmark_marker",flat=True))
            print("getAllBookmakerLocationQuery",bookmarkList)


            return JsonResponse(bookmarkList,safe = False)

        except Exception as e:
            raise e
            
    return HttpResponse()


@api_view(['POST'])
def updateBookmakerLocationQuery(request):
    if request.method == 'POST':
        try:

            data_dict = request.POST
            data_dict = dataRefacter(data_dict)
            user_id = returnUserIdFromToken(data_dict['token'])
            marker_id = data_dict['markerId']
            is_bookmarked = data_dict['isBookmarked']

            print("updateBookmaker",data_dict)
            get_User = User.objects.get(student_id=user_id)
            get_Marker = Marker.objects.get(id=int(marker_id))

            if(is_bookmarked == 'true'): #create
                saveBookmark = Bookmark.objects.create(bookmark_student=get_User,bookmark_marker=get_Marker,createtime=datetime.now())
                print("save Bookamerk ",saveBookmark)
            elif(is_bookmarked == 'false'):
                getBookmark = Bookmark.objects.filter(bookmark_student=user_id,bookmark_marker=marker_id)
                getBookmark.delete()

            #get_User = User.objects.get(student_id=user_id)
            
            # saveLike = MarkerLike.objects.create(markerlike_marker=get_Marker,markerlike_student=get_User)

        except Exception as e:
            raise e
            
    return HttpResponse()