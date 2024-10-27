from rest_framework.views import APIView
from rest_framework.response import Response

class GoogleAuthView(APIView) :

    def get(self, request) : 
        return Response({
            'url' : "google_auth_url"
        })
    

class FacebookAuthView(APIView) :

    def get(self, request) : 
        return Response({
            'url' : "facebook_auth_url"
        })
    
