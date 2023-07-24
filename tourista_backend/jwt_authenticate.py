# backends.py

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import RevokedToken, Host


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')


        if not auth_header:
            return None

        token = auth_header.split(' ')[0]

        try:
            # Verify the token and get the user payload
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('id')
            # Check if the token is blacklisted
            if RevokedToken.objects.filter(token=token).exists():
                raise AuthenticationFailed('Invalid token.')

            # Retrieve and return the user object
            # Replace 'CustomUser' with your custom user model
            user = Host.objects.get(id=user_id)
            return user, token

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            print("invalid")
            raise AuthenticationFailed('Invalid token.')
        except Host.DoesNotExist:
            raise AuthenticationFailed('No user found for the provided token.')

        return None
