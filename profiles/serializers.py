from rest_framework import serializers
from .models import Profile
from followers.models import Follower
from followrequests.models import FollowRequest  # Import FollowRequest model

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    milestones_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_private = serializers.BooleanField(required=False)
    can_view_posts = serializers.SerializerMethodField()
    can_view_milestones = serializers.SerializerMethodField()
    request_sent = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count', 
            'milestones_count', 'is_private', 'can_view_posts',
            'can_view_milestones', 'request_sent',
        ]

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner  # Ensure `owner` field matches the model
            ).first()
            return following.id if following else None
        return None

    def get_can_view_posts(self, obj):
        # Access the dynamic attribute set in the view
        return getattr(obj, 'can_view_posts', True)

    def get_can_view_milestones(self, obj):
        # Access the dynamic attribute set in the view
        return getattr(obj, 'can_view_milestones', True)

    def get_request_sent(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FollowRequest.objects.filter(
                requester=user, receiver=obj.owner, status='pending'  # Ensure `owner` field matches the model
            ).exists()
        return False
