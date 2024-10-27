"""
    ALl avaliable platforms for social auth

"""

from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseSocialPlatform(ABC) : 
    
    @abstractmethod
    def get_access_token(self) : ...

    @abstractmethod
    def get_auth_url(self) : ...


class GoogleAuth(BaseSocialPlatform) : 

    def get_access_token(self):
        pass

    def get_auth_url(self):
        return super().get_auth_url()


class FacebookAuth(BaseSocialPlatform):

    def get_access_token(self):
        pass

    def get_auth_url(self):
        return super().get_auth_url()