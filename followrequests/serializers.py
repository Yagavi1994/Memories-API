from rest_framework import serializers
from .models import FollowRequest
from django.contrib.auth.models import User


class FollowRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the FollowRequest model.
    """
    # Fields for requester and receiver
    requester = serializers.ReadOnlyField(source='requester.username')
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )  # noqa

    # Profile image and username of the requester
    requester_profile_image = serializers.SerializerMethodField()
    requester_username = serializers.ReadOnlyField(
        source="requester.username"
    )

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
        """
        Returns the absolute URL of the requester's profile image if available.
        """
        if obj.requester.profile.image: 
            request = self.context.get('request')
            return request.build_absolute_uri(obj.requester.profile.image.url)
        return None 

    def validate(self, data):
        """
        Prevent users from sending follow requests to themselves.
        """
        if self.context['request'].user == data.get('receiver'):
            raise serializers.ValidationError(
                "You cannot send a follow request to your own profile."
            )
        return data
