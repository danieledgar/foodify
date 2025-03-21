import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import os
from django.conf import settings
from dotenv import load_dotenv

env_path = os.path.join(settings.BASE_DIR ,'lets_bite','.env')
load_dotenv(env_path)


class MpesaCredentials:
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    api_url = os.getenv('API_URL')
    

class MpesaAccessToken:
    @classmethod
    def get_mpesa_access_token(cls):
        r = requests.get(
            MpesaCredentials.api_url,
            auth=HTTPBasicAuth(
                MpesaCredentials.consumer_key, 
                MpesaCredentials.consumer_secret
            )
        )
        return json.loads(r.text)['access_token']
    
class MpesaPassword:
    @classmethod
    def get_lipa_time(cls):
        return datetime.now().strftime('%Y%m%d%H%M%S')

    @classmethod
    def get_decoded_password(cls):
        business_short_code = '174379'
        passkey = os.getenv('PASS_KEY')
        lipa_time = cls.get_lipa_time()
        
        data_to_encode = business_short_code + passkey + lipa_time
        online_password = base64.b64encode(data_to_encode.encode())
        return online_password.decode('utf-8')

    @classmethod
    def get_business_short_code(cls):
        return os.getenv('BUSINESS_SHORT_CODE')