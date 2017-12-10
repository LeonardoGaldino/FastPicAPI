# -*- coding: utf-8 -*-

# Django Imports
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from FastPicAPI.settings import API_KEY, API_VERSION, API_URL
from django.db import IntegrityError
# Custom imports
import json
import requests
from models import OnlineUser
from http_status_codes import OK, BAD_REQUEST, NOT_FOUND, INTERNAL_SERVER_ERROR

# Views

@csrf_exempt
@require_http_methods(["POST"])
def v_upload_image(request):
    uploaded_img = request.FILES.get('img', None)
    if uploaded_img == None:    
        return JsonResponse({'error': True, 'errorMessage': 'No image uploaded!'}, safe=False, status=BAD_REQUEST)

    img_type = uploaded_img.name.split('.')[-1]
    img_name = 'uploaded_img.'+img_type
    mime_type = 'image/' + img_type
    imgs = { 'images_file': (img_name, uploaded_img.read(), mime_type) }
    req_header_params = {
        'api_key': API_KEY,
        'version': API_VERSION
    }
    req = requests.post(API_URL, params=req_header_params, files=imgs)

    return JsonResponse({'error': False, 'content': req.content}, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def v_get_online_users(request):
    try:
        online_users = list(OnlineUser.objects.all().values('name', 'points'))
        return JsonResponse({'error': False, 'content': online_users}, safe=False)
    except:
        return JsonResponse({'error': True, 'messageError': 'Internal Server Error'}, safe=False, status=INTERNAL_SERVER_ERROR)

''' Comentado porque na reuniao, acordamos que pro MVP
    so teriamos uma unica sala, que todos os usuarios entrarão ao entrar no site.

@require_http_methods(["POST"])
def create_room(request):
    room_data = json.loads(request.body)
    if room_data.get("name") and room_data.get("owner_name"):
        if Room.objects.filter(name=room_data.get("name")).count() > 0:
            return JsonResponse({"error_message": "room with this name already created"}, status=400)

        room = Room(name=room_data.get("name"), owner_name=room_data.get("owner_name"))
        room.save()
        return JsonResponse({"message": "room was created"}, safe=False)
    else:
        return JsonResponse({"error_message": "insuficient data to create room"}, safe=False,
                            status=400)
'''

@csrf_exempt
@require_http_methods(["POST"])
def v_enter_room(request):
    user_name = request.POST.get('userName', None)
    if user_name == None:
        return JsonResponse({'error': True, 'messageError': 'No username uploaded!'}, safe=False, status=BAD_REQUEST)
    try:
        OnlineUser.objects.create(name=user_name, points=0)
    except IntegrityError:
        #Catches username duplicated problem
        return JsonResponse({'error': True, 'messageError': 'Username already taken!'}, safe=False, status=BAD_REQUEST)
    return JsonResponse({'error': False, 'content': 'User registered!'}, safe=False, status=OK)
    
'''
    if request_data.get("room_name"):
        room_name = request_data.get("room_name")
        if Room.objects.filter(name=room_name):
            room = Room.objects.get(name=room_name)
            if room is not None:
                user = OnlineUser.objects.get(name=request_data.get("user_name"))
                room.participants.add(user)
                return JsonResponse(status=200)
        else:
            return JsonResponse({"error_message": "there is no room with given name"}, status=404)

    else:
        return JsonResponse({"error_message": "insuficient data to enter room"}, safe=False,
                            status=400)'''
