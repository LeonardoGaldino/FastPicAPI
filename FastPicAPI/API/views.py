# Django Imports
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from FastPicAPI.settings import API_KEY, API_VERSION, API_URL
from .models import Room

# Custom imports
import json
import requests

# Views

@csrf_exempt
@require_http_methods(["GET", "POST"])
def v_upload_image(request):
    if request.method == 'GET':
        json_object = [{
            'Leo': True
        },
        {
            'Bormann': False
        }]

        # Safe param equals False to send non dict objects
        return JsonResponse(json_object, safe=False)
    
    # At this point, only method POST
    uploaded_img = request.FILES['img']
    imgs = [('images_file', ('temp.jpg', uploaded_img.read(), 'image/jpg'))]
    req_header_params = {
        'api_key': API_KEY,
        'version': API_VERSION
    }
    req = requests.post(API_URL, params=req_header_params, files=imgs)

    return JsonResponse(req.content, safe=False)


@require_http_methods(["POST"])
def create_room(request):
    room_data = json.loads(request.body)
    if room_data.get("name") and room_data.get("owner_name"):

        if Room.objects.get(name=room_data.get("name")):
            return JsonResponse({"error_message": "room with this name already created"}, status=400)

        room = Room(name=room_data.get("name"), owner_name=room_data.get("owner_name"))
        room.save()
        return JsonResponse({"message": "room was created"}, safe=False)
    else:
        return JsonResponse({"error_message": "insuficient data to create room"}, safe=False,
                            status=400)


@require_http_methods(["GET", "POST"])
def enter_room(request):

    return None
