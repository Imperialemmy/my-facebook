from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="cover_photos/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        blank=True, null=True
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    relationship_status = models.CharField(
        max_length=20,
        choices=[
            ("Single", "Single"),
            ("In a Relationship", "In a Relationship"),
            ("Married", "Married"),
            ("It's Complicated", "It's Complicated"),
        ],
        blank=True, null=True
    )
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    is_private = models.BooleanField(default=False)
    allow_messages = models.BooleanField(default=True)
    about_me = models.TextField(blank=True, null=True)

    def friends_count(self):
        return self.friends.count()

    def __str__(self):
        return self.username

class Work(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="work_experiences")
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # If still working there, this can be null

    def __str__(self):
        return f"{self.user.username} - {self.position} at {self.company}"

class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="education_history")
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True, null=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.school} ({self.start_year} - {self.end_year})"

class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")],
        default="pending"
    )

    def accept(self):
        """Accepts the friend request and updates friendships"""
        self.status = "accepted"
        self.save()
        self.sender.friends.add(self.receiver)  # Add to friends list
        self.receiver.friends.add(self.sender)

    def decline(self):
        """Declines the friend request"""
        self.status = "declined"
        self.delete()  # Remove the request

    def cancel(self):
        """Cancels the friend request (used by sender)"""
        self.delete()

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"