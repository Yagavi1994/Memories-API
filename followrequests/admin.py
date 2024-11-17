from django.contrib import admin
from django.utils.html import format_html
from .models import FollowRequest

@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'requester', 'receiver', 'status', 'created_at', 'requester_profile_image']
    list_filter = ['status', 'created_at']
    search_fields = ['requester__username', 'receiver__username']

    def requester_profile_image(self, obj):
        if obj.requester.profile.image:  # Assuming the profile model has an `image` field
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.requester.profile.image.url
            )
        return "No Image"

    requester_profile_image.short_description = "Requester Profile Image"
