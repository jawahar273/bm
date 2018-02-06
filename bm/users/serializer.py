import urllib, hashlib

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from .models import UserProfileSettings

User = get_user_model()

class UserSerializer(UserDetailsSerializer):
    '''
    The user serializer is child of :model: `rest_auth.UserDetailsSerializer`
    which is an extenstion. To generate gravatar url based on the given
    email.
    '''
    profile_url = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile_url',)
        read_only_fields =UserDetailsSerializer.Meta.read_only_fields + ('username',)

    def get_profile_url(self, object):
        const_url = "https://www.gravatar.com/avatar/"
        # IPython.embed()
        url = object.email.lower().encode()
        url = hashlib.md5(url).hexdigest()
        return '{}{}?d=identicon'.format(const_url, url)

class UserProfileSettingsSerializer(object):
    '''
    The profile setting is not stable yet.
    '''
    class Meta:
        fields = '__all__'
        read_only_fields = ('email',)
            