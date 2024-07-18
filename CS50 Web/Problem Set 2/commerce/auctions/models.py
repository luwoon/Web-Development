from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass 


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_listings', default='')
    title = models.CharField(max_length=100)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.CharField(max_length=1000, default='')
    created_time = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=64, default='')
    closed = models.BooleanField(default=False)
    winning_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winning_listings', null=True, blank=True)
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.title} from ${self.starting_bid}"


class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amt = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(default='')
    time = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')