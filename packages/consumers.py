
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

        # setting the channel name
        # remeber don't set channel name in __init__
        self.channel_name = 'bm.notification.channel'
        self.user = self.scope["user"]
        import IPython
        IPython.embed()
        if self.user.is_anonymous:
            await self.close()

        await self.accept()

    async def receive(self, text_data=None):
        # print('receive: ', self.channel_name)
        pass

    async def disconnect(self, close_code):
        pass

    async def upload_status(self, event):
        status = event['status']
        print('status=>', status)

        await self.send(text_data=status)

