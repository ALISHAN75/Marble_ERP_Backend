from rest_framework import renderers
import json
from rest_framework.response import Response
from googletrans import Translator
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate



class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            if "[ErrorDetail(string='A valid integer is required.', code='invalid')]" in str(data)  or "[ErrorDetail(string='user with this Email already exists.', code='unique')]" in str(data) or  "[ErrorDetail(string='This field is required.', code='required')]" in str(data):       
                try:
                    data_ur = str(data)
                    if "[ErrorDetail(string='A valid integer is required.', code='invalid')]" in data_ur:
                        data_ur = data_ur.replace("[ErrorDetail(string='A valid integer is required.', code='invalid')]" , "['ایک درست عدد درکار ہے۔']")
                        data_ur = data_ur.replace("\'", "\"")
                        data_ur = json.loads(data_ur)
                    if "[ErrorDetail(string='user with this Email already exists.', code='unique')]" in data_ur:
                        data_ur = data_ur.replace("[ErrorDetail(string='user with this Email already exists.', code='unique')]" , "['اس ای میل کے ساتھ صارف پہلے سے موجود ہے۔']")
                        data_ur = data_ur.replace("\'", "\"")
                        data_ur = json.loads(data_ur)
                    if "[ErrorDetail(string='This field is required.', code='required')]" in data_ur:
                        data_ur = data_ur.replace("[ErrorDetail(string='This field is required.', code='required')]" , "['اس کو پر کرنا ضروری ہے']")
                        data_ur = data_ur.replace("\'", "\"")
                        data_ur = json.loads(data_ur)
                    # for x, y in data_ur.items():
                    #     y = list(map(lambda y: y.replace('اس', x), y))
                    #     data_ur.update({x : y})
                except json.decoder.JSONDecodeError as e:
                    response = "An error occurred while decoding the JSON data in Accounts/renderers.py  :  ", str(e)          
                try:
                    
                    # for x, y in data.items():
                    #     y = list(map(lambda y: y.replace('This', x), y))
                    #     data.update({x : y})
                    response = json.dumps({
                    'error': data,
                    'error_ur':  data_ur  } )
                except json.decoder.JSONDecodeError as e:
                    response = "An error occurred while decoding the JSON data in Accounts/renderers.py :", str(e)
            else:
                response = json.dumps(data , default=str)
        else:
            response = json.dumps(data , default=str)
        return response



