from django.db import models
from users.models import CustomUser



class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender}"


class MessageMedia(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="media_files")
    file = models.FileField(upload_to="chat_media/")
