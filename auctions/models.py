from django.contrib.auth.models import AbstractUser
from django.db import models


# superuser: superjosh pass: 123

# Model for users
class User(AbstractUser):
    pass

# Model for categories
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

# Model for auction listings
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    startbid = models.IntegerField()
    photo_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
    available = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")
    

    def __str__(self):
        return f'{self.id}: {self.title}'

# Model for comments
class Comment(models.Model):
    content = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default=None)

    def __str__(self):
        return f'{self.commenter}: {self.content}'

# Model for watchlists
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    watched_listings = models.ManyToManyField(Listing, related_name="listings", blank=True)

    def __str__(self):
        return f'{self.user}\'s watchlist'

# Model for Bids
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    price = models.IntegerField()

    def __str__(self):
        return f'{self.price} on {self.listing}'