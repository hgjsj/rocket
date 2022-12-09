from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User

class TokenServiceAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTH_TOKEN")
        if token:
            return User.objects.get(username='admin'), token
        else:
            return None
