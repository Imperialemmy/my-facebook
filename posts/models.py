from django.db import models
from django.conf import settings
from users.models import CustomUser


class Post(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('only_me', 'Only Me'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False, null=False)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    shared_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    tagged_users = models.ManyToManyField(CustomUser, related_name="tagged_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class PostImage(models.Model):
    post_picture = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_images")
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"Image for {self.post_picture.user.username}'s post"


class PostVideo(models.Model):
    post_video = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_videos")
    video = models.FileField(upload_to='post_videos/')

    def __str__(self):
        return f"Video for {self.post_video.user.username}'s post"

class Stories(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    image = models.ImageField(upload_to='post_comments_images/',null=True,blank=True)
    video = models.FileField(upload_to='post_comments_videos/',null=True,blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.user.username}'s post"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    created_at = models.DateTimeField(auto_now_add=True)

class Emoji(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_emojis")
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
