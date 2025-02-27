import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from users.models import CustomUser
from .models import Message, MessageMedia, Conversation, MessageReactions


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles WebSocket connection"""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f" WebSocket Connected to: {self.room_group_name}")

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f" WebSocket Disconnected from: {self.room_group_name}")

    async def receive(self, text_data):
        """Handles incoming WebSocket messages"""
        data = json.loads(text_data)
        event_type = data.get("type")

        if event_type == "send_reaction":
            await self.handle_reaction(data)

        elif event_type == "chat_typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_typing",
                    "sender": self.scope["user"].username,
                }
            )

        elif event_type == "chat_stop_typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_stop_typing",
                    "sender": self.scope["user"].username,
                }
            )

        elif event_type == "mark_as_read":
            await self.mark_message_as_read(data)

        if event_type == "send_message":
            await self.handle_send_message(data)

    async def mark_message_as_read(self, data):
        """Marks a message as read and notifies others"""
        message_id = data.get("message_id")

        message = await database_sync_to_async(Message.objects.get)(id=message_id)
        message.is_read = True
        await database_sync_to_async(message.save)()

        # Broadcast read status
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "message_read",
                "message_id": message_id,
            }
        )

    async def message_read(self, event):
        """Broadcasts message read status to WebSocket clients"""
        await self.send(text_data=json.dumps({
            "type": "message_read",
            "message_id": event["message_id"],
        }))

    async def handle_send_message(self, data):
        """Handles sending messages"""
        username = data.get("username")
        content = data.get("content", "")
        media_urls = data.get("media_urls", [])

        # Validate user and conversation
        user = await sync_to_async(CustomUser.objects.get)(username=username)
        conversation = await sync_to_async(Conversation.objects.get)(id=self.room_name)

        # Save the message in the database
        new_message = await sync_to_async(Message.objects.create)(
            sender=user, content=content, conversation=conversation
        )

        # Save media files
        for url in media_urls:
            await sync_to_async(MessageMedia.objects.create)(
                message=new_message,
                file=url  # Assuming frontend sends file URLs after upload
            )

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_id": new_message.id,
                "message": new_message.content,
                "media_urls": media_urls,
                "sender": user.username,
                "timestamp": str(new_message.timestamp),
            }
        )

    async def chat_typing(self, event):
        """Broadcasts typing status to other users"""
        await self.send(text_data=json.dumps({
            "type": "chat_typing",
            "sender": event["sender"],
        }))

    async def chat_stop_typing(self, event):
        """Broadcasts stop typing status to other users"""
        await self.send(text_data=json.dumps({
            "type": "chat_stop_typing",
            "sender": event["sender"],
        }))

    async def handle_reaction(self, data):
        """Handles a reaction being added or removed"""
        message_id = data.get("message_id")
        emoji = data.get("emoji")
        user = self.scope["user"]

        if not user.is_authenticated:
            return

        message = await database_sync_to_async(Message.objects.get)(id=message_id)

        # Get or create reaction
        reaction, created = await database_sync_to_async(MessageReactions.objects.get_or_create)(
            message=message, user=user, defaults={"emoji": emoji}
        )

        if not created:
            if reaction.emoji == emoji:
                # Remove reaction if the same emoji is clicked again
                await database_sync_to_async(reaction.delete)()
                action = "removed"
            else:
                # Update emoji if different
                reaction.emoji = emoji
                await database_sync_to_async(reaction.save)()
                action = "updated"
        else:
            action = "added"

        # Broadcast reaction update
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_reaction",
                "message_id": message_id,
                "emoji": emoji,
                "user": user.username,
                "action": action,
            }
        )

    async def chat_reaction(self, event):
        """Sends a reaction update to WebSocket clients"""
        await self.send(text_data=json.dumps(event))

    async def chat_message(self, event):
        """Sends a message to WebSocket clients"""
        await self.send(text_data=json.dumps({
            "message_id": event["message_id"],
            "message": event["message"],
            "media_urls": event["media_urls"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))
