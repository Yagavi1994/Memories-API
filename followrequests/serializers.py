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
        ]

    def get_requester_profile_image(self, obj):
        if obj.requester.profile.image:  # Assuming the Profile model has an image field
            request = self.context.get('request')
            # Generate absolute URL for the image
            return request.build_absolute_uri(obj.requester.profile.image.url)
        return None  # Return None if no profile image is set
           
    def validate(self, data):
        # Prevent users from sending follow requests to themselves
        if self.context['request'].user == data.get('receiver'):
            raise serializers.ValidationError("You cannot send a follow request to your own profile.")
        return data
