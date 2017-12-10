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
@require_http_methods(["POST"])
def v_upload_image(request):
    uploaded_img = request.FILES.get('img', None)
    if uploaded_img == None:    
        return JsonResponse({'error': True, 'errorMessage': 'No image uploaded!'}, safe=False)

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
