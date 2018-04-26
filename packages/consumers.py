
from django.core.cache import cache
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.auth import get_user


class BMNotifcationConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    # def __init__(self, *args):
    #     import IPython
    #     IPython.embed()

    async def connect(self, *args, **kwars):

        self.channel_name = 'bm'
        await self.accept()
        print(self.channel_name)
        # sync_to_async(cache.set)()
        # await sync_to_async(cache.set)()


    async def receive(self, text_data=None):

        # await self.send(text_data=text_data)
        # print(text_data, get_user(self.scope))
        print('receive: ', self.channel_name)

    async def disconnect(self, close_code):
        pass

    async def upload_status(self, event):
        status = event['status']
        print('status=>', status)

        await self.send(text_data=status)

