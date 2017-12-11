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
from utils import classify_img, extract_classes

# Views

@csrf_exempt
@require_http_methods(["POST"])
def v_upload_image(request):
    uploaded_img = request.FILES.get('img', None)
    if uploaded_img == None:    
        return JsonResponse({'error': True, 'errorMessage': 'No image uploaded!'}, safe=False, status=BAD_REQUEST)

    fetched_json = classify_img(uploaded_img)
    classes = extract_classes(fetched_json)

    return JsonResponse({'error': False, 'content': classes})

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
        current_object = PictureTarget.objects.all().values('name')
        if len(current_object):
            return JsonResponse({'error': False, 'content': current_object[0]}, safe=False)
        return JsonResponse({'error': False, 'content': {}}, safe=False)
    except:
        return JsonResponse({'error': True, 'messageError': 'Internal Server Error'}, safe=False, status=INTERNAL_SERVER_ERROR) 

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

@csrf_exempt
@require_http_methods(["POST"])
def v_leave_room(request):
    user_name = request.POST.get('userName', None)
    if user_name == None:
        return JsonResponse({'error': True, 'messageError': 'No username uploaded!'}, safe=False, status=BAD_REQUEST)
    try:
        user = OnlineUser.objects.get(name=user_name)
        user.delete()
    except ObjectDoesNotExist:
        return JsonResponse({'error': True, 'messageError': 'User does not exists!'}, safe=False, status=BAD_REQUEST)
    return JsonResponse({'error': False, 'content': 'User left!'}, safe=False, status=OK)
    