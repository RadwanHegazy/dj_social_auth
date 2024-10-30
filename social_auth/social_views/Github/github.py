from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from social_auth.platforms import GitHubAuth
from .serializers import GithubCodeSerializer

class GithubAuthView(CreateAPIView) :
    serializer_class = GithubCodeSerializer
    queryset = []

    def get_serializer_context(self):
        print(self.request.get_full_path_info())
        pass

class CreateGithubAuthLinkView(APIView) :
    __github_auth = GitHubAuth()

    def get (self, request) : 
        return Response({
            'url' : self.__github_auth.get_auth_url()
        })