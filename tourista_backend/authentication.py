# your_app/authentication.py
from rest_framework.authentication import TokenAuthentication

class GetMethodTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if request.method == 'GET':
            return super().authenticate(request)
        return None
