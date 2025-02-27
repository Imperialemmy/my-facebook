import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from messaging.models import Message, Conversation, MessageMedia
from users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles WebSocket connection"""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # Join the chat group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        """Handles incoming WebSocket messages"""
        message_text = content.get("content", "")
        username = content.get("username")
        media_urls = content.get("media_urls", [])

        # Validate user and conversation
        user = await sync_to_async(CustomUser.objects.get)(username=username)
        conversation = await sync_to_async(Conversation.objects.get)(id=self.room_name)

        # Save the message in the database
        new_message = await sync_to_async(Message.objects.create)(
            sender=user, content=message_text, conversation=conversation
        )

        # Save media files if provided
        media_objects = []
        for url in media_urls:
            media = await sync_to_async(MessageMedia.objects.create)(
                message=new_message,  # Use the actual Message instance
                file=url
            )
            media_objects.append(media)

        # Broadcast message to the WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_id": new_message.id,
                "message": new_message.content if new_message.content else None,
                "media_urls": media_urls,
                "sender": user.username,
                "timestamp": str(new_message.timestamp),
            }
        )

    async def chat_message(self, event):
        """Sends a message to WebSocket clients"""
        await self.send_json({
            "message_id": event["message_id"],
            "message": event["message"],
            "media_urls": event["media_urls"] or [],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        })
