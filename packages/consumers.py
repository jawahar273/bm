import asyncio

from django.core.cache import cache

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.exceptions import ValidationError

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import get_user

from packages.utils import to_query_string_dict


class BMNotifcationConsumer(AsyncWebsocketConsumer):
    """Bm Notification is a async web socket class
    which is used to send the notificaion to client app.
    
    :param groups: [name of the group]
    :type groups: list

    ChangeLog:
        -- Wednesday 09 May 2018 08:44:15 AM IST
        @jawahar273 [Version 0.3]
        -1- Removing the __init__ of the class.
    """
    groups = ["broadcast"]

    async def connect(self):
        """This method is called on init connection
        between the client and server.
        
        .. notes:
            Channel name not be set in `__init__`. If you know
            what are you doing.

        ChangeLog:
            -- Wednesday 09 May 2018 08:50:05 AM IST
            @jawahar273 [Version 0.3]
            -1- Updating docset.

        """

        self.channel_name = "bm.notification.channel"
        query_string = to_query_string_dict(self.scope["query_string"])
        self.JWTtoken = query_string["token"]
        user_status = self.validation_jwt(self.JWTtoken)

        if not user_status["status"]:

            await self.accept()
            await asyncio.sleep(1)
            await self.send("Unauthenticated user. " "Connection closing")
            await self.close()

        else:

            await self.accept()
            # await self.upload_status({'status': '45'})
            # await self.upload_status({'status': '125'})
            # await self.upload_status({'status': '434'})

    def validation_jwt(self, value):
        """This method validate the given token
        as its from the authencated user's. 
        
        :param value: [JWT token from the client]
        :type value: [str]

        ChangeLog:
            -- Wednesday 09 May 2018 08:47:08 AM IST
            @jawahar273 [Version 0.3]
            -1- rename {valitication_jwt => validation_jwt}
        """
        try:

            result = VerifyJSONWebTokenSerializer().validate({"token": value})

            return {"status": True, "user": result["user"]}

        except ValidationError:

            return {"status": False}

    async def receive(self, text_data=None):

        pass

    async def disconnect(self, close_code):

        pass

    async def upload_status(self, event):

        status = event["status"]

        await self.send(text_data=status)
