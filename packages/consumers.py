import asyncio
from django.core.cache import cache
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.auth import get_user


class BMNotifcationConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self, *args, **kwars):

        # setting the channel name
        # remeber don't set channel name in __init__
        self.channel_name = 'bm.notification.channel'
        self.user = self.scope["user"]
        user_status = self.is_anonymous(self.user)
        # print('user permission', user_status == True)

        if user_status:

            await self.accept()
            await asyncio.sleep(1)
            await self.send('Unauthenticated user. Connection closing')
            await self.close()

        else:
            await self.accept()

    async def is_anonymous(self, value):
        return value.is_anonymous

    async def receive(self, text_data=None):
        pass

    async def disconnect(self, close_code):
        pass

    async def upload_status(self, event):
        status = event['status']
        print('status=>', status)

        await self.send(text_data=status)

