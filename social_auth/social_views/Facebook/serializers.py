from rest_framework import serializers
from social_auth.platforms import FacebookAuth, generate_tokens_for_user
from django.contrib.auth import get_user_model

User = get_user_model()

class FacebookSerializer (serializers.Serializer) : 
    access_token = serializers.CharField()
    __fb_auth = FacebookAuth()
    
    def create(self, validated_data):
        access_token = validated_data.get('access_token')
        user = self.__fb_auth.get_user_info_by_accessToken(access_token)
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

        return site_user
    
    def to_representation(self, instance):
        tokens = generate_tokens_for_user(instance)
        return tokens

