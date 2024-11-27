from rest_framework import serializers
from .models import Profile
from followers.models import Follower
from followrequests.models import FollowRequest


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Includes dynamic fields for post/milestone visibility,
    follow status, and more.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_pk = serializers.ReadOnlyField(source='owner.pk')
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

    def get_is_owner(self, obj):
        """
        Check if the requesting user is the owner of the profile.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        """
        Retrieve the ID of the Follower instance if the requesting user follows
        the profile's owner.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_can_view_posts(self, obj):
        """
        Determine if the requesting user can view the profile's posts.
        """
        return getattr(obj, 'can_view_posts', True)

    def get_can_view_milestones(self, obj):
        """
        Determine if the requesting user can view the profile's milestones.
        """
        return getattr(obj, 'can_view_milestones', True)

    def get_request_sent(self, obj):
        """
        Check if the requesting user has sent
        a follow request to the profile's owner.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            return FollowRequest.objects.filter(
                requester=user, receiver=obj.owner, status='pending'
            ).exists()
        return False

    class Meta:
        model = Profile
        fields = [
            'id', 'profile_pk', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id', 'posts_count',
            'followers_count', 'following_count', 'milestones_count',
            'is_private', 'can_view_posts', 'can_view_milestones',
            'request_sent',
        ]
