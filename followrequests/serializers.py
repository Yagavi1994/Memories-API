from rest_framework import serializers
from .models import FollowRequest

class FollowRequestSerializer(serializers.ModelSerializer):
    requester = serializers.ReadOnlyField(source='requester.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')
    requester_profile_image = serializers.CharField(source="requester.profile_image.url", read_only=True)
    requester_username = serializers.CharField(source="requester.username", read_only=True)

    class Meta:
        model = FollowRequest
        fields = ['id', 'requester', 'receiver', 'requester_profile_image', 'requester_username', 'status', 'created_at']
