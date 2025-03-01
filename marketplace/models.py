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
    stock = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def update_availability(self):
        if self.stock > 0:
            self.is_available = True
        else:
            self.is_available = False
        self.save()

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


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('shipped', 'Shipped')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Reduce stock when an order is placed. """
        if self.pk is None:  # Only reduce stock on NEW orders
            if self.listing.stock >= self.quantity:
                self.listing.stock -= self.quantity
                self.listing.update_availability()
                self.listing.save()
            else:
                raise ValueError("Not enough stock available")
        super().save(*args, **kwargs)


class Refund(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="refunds")
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('refunded', 'Refunded')],
        default='requested'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Increase stock when a refund is requested. """
        if self.pk is None:  # Only increase stock on NEW refund requests
            self.order.listing.stock += self.order.quantity
            self.order.listing.update_availability()
            self.order.listing.save()
        super().save(*args, **kwargs)

    def approve(self):
        """ Mark the refund as approved and issue refund logic """
        self.status = "accepted"
        self.save()

    def reject(self):
        """ Reject the refund request """
        self.status = "rejected"
        self.save()

    def process_refund(self):
        """ Handle refund processing (e.g., update order/payment status) """
        if self.status == "accepted":
            self.status = "refunded"
            # Add logic here to refund payment
            self.save()


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()  # Or a choices field for specific ratings
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.title} - {self.rating}⭐"