import asyncio

from django.core.cache import cache

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.exceptions import ValidationError

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import get_user

from packages.utils import to_query_string_dict


class BMNotifcationConsumer(AsyncWebsocketConsumer):
    '''Bm Notification is a async web socket class
    which is used to send the notificaion to client app.
    
    :param groups: [name of the group]
    :type groups: list
    '''
    groups = ["broadcast"]

    async def connect(self):

        # setting the channel name
        # remeber, don't set channel name in __init__

        self.channel_name = 'bm.notification.channel'

        query_string = to_query_string_dict(self.scope['query_string'])
        self.JWTtoken = query_string['token']
        user_status = self.valitication_jwt(self.JWTtoken)

        if not user_status['status']:

            await self.accept()
            await asyncio.sleep(1)
            await self.send('Unauthenticated user. '
                            'Connection closing')
            await self.close()

        else:

            await self.accept()

    def valitication_jwt(self, value):
        try:

            result = VerifyJSONWebTokenSerializer.validate({'token': value})

            return {

                'status': True,
                'user': result['user']

            }

        except ValidationError:

            return {

                'status': False

            }

    async def receive(self, text_data=None):

        pass

    async def disconnect(self, close_code):

        pass

    async def upload_status(self, event):

        status = event['status']
        print('status=>', status)

        await self.send(text_data=status)

