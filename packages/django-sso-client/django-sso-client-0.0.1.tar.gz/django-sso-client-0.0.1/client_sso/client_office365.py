from django.http import HttpResponseRedirect
from client_base import ClientBase
import requests

class ClientOffice365(ClientBase):

    def login(self,token:str):
        response = HttpResponseRedirect(f'{self.host}/office365/callback/')
        response['Authorization'] = f'Bearer {token}'
        return response