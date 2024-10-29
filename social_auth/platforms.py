"""
    ALl avaliable platforms for social auth

"""

from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import ValidationError
import requests
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class BaseSocialPlatform(ABC) : 
    
    @abstractmethod
    def get_access_token(self) : ...

    @abstractmethod
    def get_auth_url(self) : ...



def generate_tokens_for_user(user) -> dict:
    tokens = RefreshToken.for_user(user)

    return {
        'refresh_token':str(tokens),
        'access_token' : str(tokens.access_token) 
    }

class GoogleAuth(BaseSocialPlatform) : 
    GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
    GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
    GOOGLE_SOCIAL_AUTH = settings.SOCIAL_AUTH['google']
    GOOGLE_REDIRECT_URL = GOOGLE_SOCIAL_AUTH['redirect_url']

    def get_access_token(self, code):
        data = {
            'code': code,
            'client_id': self.GOOGLE_SOCIAL_AUTH['client_id'],
            'client_secret': self.GOOGLE_SOCIAL_AUTH['client_secret'],
            'redirect_uri': self.GOOGLE_REDIRECT_URL,
            'grant_type': 'authorization_code'
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok : 
            raise ValidationError('Failed to get access token from google')

        json_data = response.json()
        return json_data['access_token']
    
    def get_user_info_by_code(self, code):
        access_token = self.get_access_token(code) 
        response = requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={'access_token' : access_token}
        )

        if not response.ok :
            raise ValidationError("Failed to get user information with tokens from google")
        
        return response.json()

    def get_auth_url(self):
        client_id = self.GOOGLE_SOCIAL_AUTH['client_id']
        url = f"https://accounts.google.com/o/oauth2/v2/auth?scope=email%20profile&access_type=offline&redirect_uri={self.GOOGLE_REDIRECT_URL}&response_type=code&client_id={client_id}"
        return url


class FacebookAuth(BaseSocialPlatform):

    def get_access_token(self):
        pass

    def get_auth_url(self):
        return super().get_auth_url()