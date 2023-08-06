from rest_framework.response import Response
from functools import wraps
from client_base import ClientBase
from rest_framework import status

def validade_permission(permissions):
    def validator(func):
        @wraps
        def wrapper(request,*args,**kwargs):
            client = ClientBase()
            token = request.Meta.get('Authorizarion')
            token = token.replace('Bearer ', '')
            token_decode = client.decode_token(token)

            scope = token_decode['scope']

            for permission in permissions:
                if permission in scope:
                    return func(request, *args, **kwargs)
           
            return Response(data={'error':'UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)
            
            