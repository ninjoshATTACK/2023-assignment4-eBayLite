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
    photo_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
    available = models.BooleanField(default=True)
    

    def __str__(self):
        return f'{self.id}: {self.title}'
