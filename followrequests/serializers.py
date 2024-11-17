from rest_framework import serializers
from .models import FollowRequest

class FollowRequestSerializer(serializers.ModelSerializer):
    # Fields for requester and receiver
    requester = serializers.ReadOnlyField(source='requester.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    # Profile image and username of the requester
    requester_profile_image = serializers.SerializerMethodField()
    requester_username = serializers.ReadOnlyField(source="requester.username")

    class Meta:
        model = FollowRequest
        fields = [
            'id',
            'requester',
            'receiver',
            'requester_profile_image',
            'requester_username',
            'status',
            'created_at',
            'request_sent',
        ]

    def get_request_sent(self, obj):
        # Check if a pending follow request exists for the logged-in user
        user = self.context['request'].user
        if user.is_authenticated:
            return FollowRequest.objects.filter(
                requester=user, receiver=obj.user, status='pending'
            ).exists()
        return False

    def get_requester_profile_image(self, obj):
        # Safely return the profile image URL or a default fallback image
        try:
            return obj.requester.profile.profile_image.url
        except AttributeError:
            # Fallback URL for missing profile images
            return "https://res.cloudinary.com/dz60wxmka/image/upload/v1730812795/media/images/Profile-pic_dxmgt2.webp"

    def validate(self, data):
        # Prevent users from sending follow requests to themselves
        if self.context['request'].user == data.get('receiver'):
            raise serializers.ValidationError("You cannot send a follow request to your own profile.")
        return data
