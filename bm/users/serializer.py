import urllib, hashlib

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from .models import UserProfileSettings

User = get_user_model()

# import IPython 

class UserSerializer(UserDetailsSerializer):

    profile_url = serializers.SerializerMethodField()

    def get_profile_url(self, object):
        const_url = "https://www.gravatar.com/avatar/"
        # IPython.embed()
        url = object.email.lower().encode()
        url = hashlib.md5(url).hexdigest()
        return '{}{}?d=identicon'.format(const_url, url)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile_url',)
        read_only_fields =UserDetailsSerializer.Meta.read_only_fields + ('username',)

class UserProfileSettingsSerializer(object):
    """docstring for UserProfileSettingsSerializer"""
    class Meta:
        fields = '__all__'
        read_only_fields = ('email',)
            