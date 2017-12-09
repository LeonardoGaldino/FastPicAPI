# Django Imports
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from FastPicAPI.settings import API_KEY, API_VERSION, API_URL

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
