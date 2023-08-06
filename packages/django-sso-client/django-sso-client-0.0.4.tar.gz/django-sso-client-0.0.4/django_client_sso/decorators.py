from rest_framework.response import Response
from functools import wraps
from django_client_sso.client_base import ClientBase
from rest_framework import status

def validator_with_request(permissions):
    def decorator_func(func):
        @wraps(func)
        def wrapper(self, request):
            client = ClientBase()
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token.replace('Bearer ', '')
            
            try:
                token_decode = client.decode_token(token)
            except Exception as ex:
                return Response(data={'error':ex.args}, status=status.HTTP_401_UNAUTHORIZED)

            required = str(permissions).split()
            scope = token_decode['scope']

            for r in required:
                if r in scope:
                    return func(self,request)
           
            return Response(data={'error':'User does not have permission to access this resource'}, status=status.HTTP_403_FORBIDDEN)
    
        return wrapper

    return decorator_func


def validator_without_request(permissions):
    def decorator_func(func):
        @wraps(func)
        def wrapper(self):
            client = ClientBase()
            token = self.request.META.get('HTTP_AUTHORIZATION')
            token = token.replace('Bearer ', '')
            
            try:
                token_decode = client.decode_token(token)
            except Exception as ex:
                return Response(data={'error':ex.args}, status=status.HTTP_401_UNAUTHORIZED)

            required = str(permissions).split()
            scope = token_decode['scope']

            for r in required:
                if r in scope:
                    return func(self)
           
            return Response(data={'error':'User does not have permission to access this resource'}, status=status.HTTP_403_FORBIDDEN)
    
        return wrapper

    return decorator_func