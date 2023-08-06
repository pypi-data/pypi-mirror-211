from rest_framework.response import Response
from functools import wraps
from django_client_sso.client_base import ClientBase
from rest_framework import status

def perm_validator(permissions):
    def decorator_func(func):
        @wraps(func)
        def wrapper(self, request):
            client = ClientBase()
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token.replace('Bearer ', '')
            token_decode = client.decode_token(token)

            required = str(permissions).split()
            scope = token_decode['scope']

            for r in required:
                if r in scope:
                    return func(self,request)
           
            return Response(data={'error':'UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)
    
        return wrapper

    return decorator_func