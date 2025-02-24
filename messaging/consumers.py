import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
import base64
from asgiref.sync import sync_to_async
from messaging.models import Message, Conversation, MessageMedia  # Import your Message model
from users.models import CustomUser



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        user = await sync_to_async(CustomUser.objects.get)(username=username)
        conversation = await sync_to_async(Conversation.objects.get)(id=self.room_name)
        new_message = await sync_to_async(Message.objects.create)(
            sender=user, content=message, conversation=conversation
        )

        if "media" in data:
            for file_data in data["media"]:  # `media` should be a list
                file_content = base64.b64decode(file_data["content"])
                file_name = f"chat_media/{username.username}_{conversation.id}_{file_data['filename']}"

                media_instance = await sync_to_async(MessageMedia.objects.create)(
                    content=message
                )
                media_instance.file.save(file_name, ContentFile(file_content))

            await self.channel_layer.group_send(
                f"chat_{conversation.id}",
                {
                    "type": "chat_message",
                    "message": message.content if message.content else None,
                    "media_urls": [media.file.url for media in await sync_to_async(list)(message.media_files.all())],
                    "sender": username.username,
                    "timestamp": str(message.timestamp),
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
