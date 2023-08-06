import requests
import jwt
from os import getenv, path

class ClientBase():
    
    def __init__(self) -> None:
        self.host = getenv('SSO_HOST','http://localhost:8000')
        self.client = getenv('CLIENT_ID','app')
        self.secret = getenv('CLIENT_SECRET','app')

    def get_app_token(self):
        data = {
            'client_id':self.client,
            'client_secret':self.secret
        }
        response = requests.post(f'{self.host}/o/token/',data=data)
        
        if response.status_code != 200:
            raise Exception(f'Erro ao tentar conectar no servidor sso. cod:{response.status_code}')
        
        return response.content['access_token']
    
    def save_public_key(self, app_token:str):
        headers = {
            'Authorization':f'Bearer {app_token}'
        }
        response = requests.get(f'{self.host}/o/token/',headers=headers)
        
        if response.status_code != 200:
            raise Exception(f'Erro ao tentar conectar no servidor sso. cod:{response.status_code}')

        with open('sso.pub','w') as file:
            file.write(response.content['data'])
            file.close()

    def decode_token(self,token:str):
        if not path.exists('ssp.pub'):
            self.save_public_key(token)

        public_key = open('sso.pub', 'r').read()
        return jwt.decode(token,key=public_key,algorithms=['RS256'])
