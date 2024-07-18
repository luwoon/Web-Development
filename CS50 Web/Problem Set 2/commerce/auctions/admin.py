from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = [field.name for field in User._meta.fields]

class ListingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Listing._meta.fields]

class BidAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bid._meta.fields]

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist)
