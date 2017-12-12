# -*- coding: utf-8 -*-

# Django Imports
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Custom imports
from models import OnlineUser, Rank, PictureTarget
from http_status_codes import OK, BAD_REQUEST, NOT_FOUND, INTERNAL_SERVER_ERROR
from utils import classify_img, extract_classes, validate_class
import json
import datetime

# Views

@csrf_exempt
@require_http_methods(["POST"])
def v_upload_image(request):
    json_data = json.loads(request.body)
    uploaded_imgB64 = json_data.get('img', None)
    mime_type = json_data.get('imgType', None)
    user_name = json_data.get('userName', None)
    if uploaded_imgB64 is None:    
        return JsonResponse({'error': True, 'errorMessage': 'No image uploaded!'}, safe=False, status=BAD_REQUEST)
    if user_name is None:
        return JsonResponse({'error': True, 'errorMessage': 'No username uploaded!'}, safe=False, status=BAD_REQUEST)
    if mime_type is None:
        return JsonResponse({'error': True, 'errorMessage': 'Image extension not specified!'}, safe=False, status=BAD_REQUEST)
    if mime_type not in ['image/jpg', 'image/gif', 'image/png', 'image/jpeg', 'image/bmp', 'image/webp']:
        return JsonResponse({'error': True, 'errorMessage': 'Image extension not valid!'}, safe=False, status=BAD_REQUEST)
    try:
        user = OnlineUser.objects.get(name=user_name)
    except ObjectDoesNotExist:
        return JsonResponse({'error': True, 'errorMessage': 'User not registered!'}, safe=False, status=BAD_REQUEST)
    fetched_json = classify_img(uploaded_imgB64, user_name, mime_type)
    classes = extract_classes(fetched_json)
    current_object = PictureTarget.objects.all()[0].name
    correct = validate_class(current_object, classes)
    if correct:
        user.points += 1
        user.save()
    return JsonResponse({'error': False, 'content': {'correct': correct}}, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def v_get_online_users(request):
    try:
        online_users = list(OnlineUser.objects.all().values('name', 'points'))
        return JsonResponse({'error': False, 'content': online_users}, safe=False)
    except:
        return JsonResponse({'error': True, 'messageError': 'Internal Server Error'}, safe=False, status=INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["GET"])
def v_get_rank(request):
    try:
        rank = Rank.objects.all().values('name', 'points')
        if len(rank):
            return JsonResponse({'error': False, 'content': rank[0]}, safe=False)
        return JsonResponse({'error': False, 'content': {}}, safe=False)
    except:
        return JsonResponse({'error': True, 'messageError': 'Internal Server Error'}, safe=False, status=INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["GET"])
def v_get_current_object(request):
    try:
        _1MINUTE = 60
        _3HOURS = 60*60*3
        current_object = PictureTarget.objects.all().values('name', 'nextChange')[0]
        current_object['nextChange'] += datetime.timedelta(seconds=_1MINUTE) 
        current_object['nextChange'] -= datetime.timedelta(seconds=_3HOURS) 
        return JsonResponse({'error': False, 'content': current_object}, safe=False)
    except:
        return JsonResponse({'error': True, 'messageError': 'Internal Server Error'}, safe=False, status=INTERNAL_SERVER_ERROR) 

@csrf_exempt
@require_http_methods(["POST"])
def v_enter_room(request):
    json_data = json.loads(request.body)
    user_name = json_data.get('userName', None)
    if user_name is None:
        return JsonResponse({'error': True, 'messageError': 'No username uploaded!'}, safe=False, status=BAD_REQUEST)
    try:
        OnlineUser.objects.create(name=user_name, points=0)
    except IntegrityError:
        #Catches username duplicated problem
        return JsonResponse({'error': True, 'messageError': 'Username already taken!'}, safe=False, status=BAD_REQUEST)
    return JsonResponse({'error': False, 'content': 'User registered!'}, safe=False, status=OK)

@csrf_exempt
@require_http_methods(["POST"])
def v_leave_room(request):
    json_data = json.loads(request.body)
    user_name = json_data.get('userName', None)
    if user_name is None:
        return JsonResponse({'error': True, 'messageError': 'No username uploaded!'}, safe=False, status=BAD_REQUEST)
    try:
        user = OnlineUser.objects.get(name=user_name)
        user.delete()
    except ObjectDoesNotExist:
        return JsonResponse({'error': True, 'messageError': 'User does not exists!'}, safe=False, status=BAD_REQUEST)
    return JsonResponse({'error': False, 'content': 'User left!'}, safe=False, status=OK)
    