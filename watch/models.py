from django.db import models
from users.models import CustomUser
# Create your models here.

#create a model for posting only videos which you can like and comment and share



class Video(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="watch_section_videos")
    video = models.FileField(upload_to='watch_videos/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s video"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="watch_section_likes")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="watch_section_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.video.user.username}'s video"

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="watch_section_comments")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="watch_section_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.video.user.username}'s video"

class Share(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="watch_section_shares")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="watch_section_shares")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} shared {self.video.user.username}'s video"


