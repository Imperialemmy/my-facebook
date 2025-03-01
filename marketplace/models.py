from django.db import models
from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="marketplace_images/")

    def __str__(self):
        return f"Image for {self.listing.title}"


class Offer(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="offers")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="offers")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer from {self.buyer.username} - {self.offer_price}"


class SavedListing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="saved_listings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="saved_by")

    def __str__(self):
        return f"{self.user.username} saved {self.listing.title}"

