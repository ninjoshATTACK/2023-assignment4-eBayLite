from django.contrib import admin

from .models import Category, Listing, Comment, Watchlist

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Watchlist)