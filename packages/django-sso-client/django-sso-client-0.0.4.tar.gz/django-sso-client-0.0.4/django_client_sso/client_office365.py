from django.http import HttpResponseRedirect
from django_client_sso.client_base import ClientBase

class ClientOffice365(ClientBase):

    def login(self,token:str):
        response = HttpResponseRedirect(f'{self.host}/office365/callback/')
        response['Authorization'] = f'Bearer {token}'
        return response