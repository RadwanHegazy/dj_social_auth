from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from .platforms import GoogleAuth, generate_tokens_for_user
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleAuthView(APIView) :
    __google_auth = GoogleAuth()

    def get_user_by_code(self, code=None) : 
        if code is None :
            return Response({
                'message' : 'invalid code'
            })

        user = self.__google_auth.get_user_info(code)

        return user
    
    def get(self, request) : 
        if 'code' in request.GET:
            code = request.GET.get('code', None)
            user = self.get_user_by_code(code)
            email = user.get('email')
            username = email.split("@")[0]
            try :
                site_user = User.objects.get(
                    email=email,
                )
            except User.DoesNotExist:
                site_user = User.objects.create(
                    email=email,
                    username=username
                )
                site_user.save()

            tokens = generate_tokens_for_user(site_user)
            return Response(tokens)
        else:
            get_url = self.__google_auth.get_auth_url()
            return Response({
                'url': get_url
            })


class FacebookAuthView(APIView) :

    def get(self, request) : 
        return Response({
            'url' : "facebook_auth_url"
        })
    
