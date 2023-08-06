import requests
from hesabe import crypt
import json

key = None
iv = None
accessCode = None
url = None


class Hesabe(object):
    def __init__(self, data):
        self.data = data

    def checkout(self):
        try:
            encrypted = crypt.encrypt(self.data, key, iv)
        except:
            return{'error': 'key or iv is incorrect please check'}
        payload = encrypted
        response = requests.request("POST", url, headers={'accessCode': accessCode}, data=payload)
        try:
            decrypted = crypt.decrypt(response.text, key, iv)
            return decrypted
        except:
            return {'error': "Authentication failed, please check access code"}
