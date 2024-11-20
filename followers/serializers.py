from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower
from django.contrib.auth.models import User


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model.
    Handles creation and ensures the unique constraint on 'owner' and 'followed'.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')
    followed_user_id = serializers.IntegerField(write_only=True)  # Accept ID for the followed user

    class Meta:
        model = Follower
        fields = [
            'id', 'owner', 'created_at', 'followed', 'followed_name', 'followed_user_id',
        ]

    def create(self, validated_data):
        try:
            # Pop the `followed_user_id` and get the user object
            followed_user_id = validated_data.pop('followed_user_id', None)
            followed_user = User.objects.get(id=followed_user_id)

            # Create the Follower instance
            return Follower.objects.create(owner=self.context['request'].user, followed=followed_user)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'You are already following this user.'})
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User does not exist.'})
