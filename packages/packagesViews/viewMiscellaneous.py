import os

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['get'])
def get_currency(request):
    '''
     get the currency symbole and representation from json
    '''
    import json
    file_location = os.path.join(settings.STATIC_ROOT, 'js', '')
    with open(file_location + 'commmon-currency.json') as file:
        return Response(json.loads(file.read()), status=status.HTTP_200_OK)
