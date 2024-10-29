from rest_framework import serializers
from social_auth.platforms import GoogleAuth, generate_tokens_for_user
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleCodeSerializer (serializers.Serializer) : 
    code = serializers.CharField()
    __google_auth = GoogleAuth()
    
    def create(self, validated_data):
        code = validated_data.get('code')
        user = self.__google_auth.get_user_info_by_code(code)
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

