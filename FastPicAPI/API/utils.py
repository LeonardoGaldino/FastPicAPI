from FastPicAPI.settings import API_KEY, API_VERSION, API_URL
import requests
import json
from base64 import decodestring


def b64toFile(img_b64, img_name, img_type):
    img_file = open(img_name+'.'+img_type, 'w')
    img_file.write(decodestring(img_b64))
    img_file.close()
    img_file = open(img_name+'.'+img_type, 'rb')
    ret = img_file.read()
    img_file.close()
    return ret

def classify_img(uploaded_img, user_name, mime_type):
    img_type = mime_type.split('/')[1]
    img_file = b64toFile(uploaded_img, user_name, img_type)
    #img_type = uploaded_img.name.split('.')[-1]
    img_name = 'uploaded_img.'+img_type
    img = { 'images_file': (img_name, img_file, mime_type) }
    req_header_params = {
        'api_key': API_KEY,
        'version': API_VERSION
    }
    req = requests.post(API_URL, params=req_header_params, files=img)
    return req.content

def extract_classes(fetched_json):
    try:
        parsed_json = json.loads(fetched_json)
        print parsed_json
        guesses = parsed_json['images'][0]['classifiers'][0]['classes']
        classes = [guess['class'].lower() for guess in guesses]
        return classes
    except Exception, e:
        f = open('errors', 'a')
        f.write(str(e)+'\n')
        f.close()
        return []

def validate_class(currentObject, classes):
    for _class in classes:
        if _class.count(currentObject) >= 1:
            return True
    return False