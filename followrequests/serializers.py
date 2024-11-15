from rest_framework import serializers
from .models import FollowRequest

class FollowRequestSerializer(serializers.ModelSerializer):
    requester = serializers.ReadOnlyField(source='requester.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = FollowRequest
        fields = ['id', 'requester', 'receiver', 'status', 'created_at']
