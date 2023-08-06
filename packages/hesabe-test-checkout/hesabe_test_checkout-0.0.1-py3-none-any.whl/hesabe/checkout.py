import requests
from crypt import encrypt, decrypt
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
            encrypted = encrypt(self.data, key, iv)
        except:
            return{'error': 'key or iv is incorrect please check'}
        payload = encrypted
        # print('encrypted data : ',encrypted)
        response = requests.request("POST", url, headers={'accessCode': accessCode}, data=payload)
        # print('response encrypted data: ', json.loads(response.text))
        if json.loads(response.text)['message'] == "Authentication failed.":
            return {'error': "Authentication failed, please check access code"}
        else:
            decrypted = decrypt(response.text, key, iv)
            return decrypted
