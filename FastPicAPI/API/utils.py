from FastPicAPI.settings import API_KEY, API_VERSION, API_URL
import requests
import json

def classify_img(uploaded_img):
    img_type = uploaded_img.name.split('.')[-1]
    img_name = 'uploaded_img.'+img_type
    mime_type = 'image/' + img_type
    img = { 'images_file': (img_name, uploaded_img.read(), mime_type) }
    req_header_params = {
        'api_key': API_KEY,
        'version': API_VERSION
    }
    req = requests.post(API_URL, params=req_header_params, files=img)

    return req.content

def extract_classes(fetched_json):
    parsed_json = json.loads(fetched_json)
    classes = parsed_json['images'][0]['classifiers'][0]['classes']
    return classes