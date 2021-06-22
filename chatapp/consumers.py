# chatapp/consumers.py

import json
from asgiref.sync import sync_to_async
from uuid import UUID

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from .models import OneonOneRoom, Message


class OneonOneChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_pk']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # message content
        message = text_data_json['message']
        # sender pk
        user_pk = text_data_json['user_pk']

        # get sender information
        user = await self.get_user_info(user_pk)

        if user.icon:
            icon_url = user.icon.url
        else:
            icon_url = None

        if message:
            # save message data
            await self.create_message_data(message, user_pk)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'icon_url': icon_url,
                    'user_name': user.username,
                    'user_pk': str(user.pk)
                }
            )

    async def chat_message(self, event):
        message = event['message']
        icon_url = event['icon_url']
        user_name = event['user_name']
        user_pk = event['user_pk']

        await self.send(text_data=json.dumps({
            'message': message,
            'icon_url': icon_url,
            'user_name': user_name,
            'user_pk': user_pk
        }))

    @sync_to_async
    def get_user_info(self, user_pk):
        user = get_user_model().objects.get(pk=UUID(user_pk))
        return user

    @database_sync_to_async
    def create_message_data(self, message, user_pk):
        try:
            room = OneonOneRoom.objects.get(pk=self.room_name)
            sender = get_user_model().objects.get(pk=UUID(user_pk))
            Message.objects.create(
                room=room,
                content=message,
                sender=sender
            )
        except Exception:
            raise HttpResponse(status=500)


class GroupChatConsumer(AsyncWebsocketConsumer):
    pass