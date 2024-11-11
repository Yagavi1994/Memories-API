from django.db import IntegrityError
from rest_framework import serializers
from likes.models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'post', 'milestone']

    def validate(self, data):
        if not data.get('post') and not data.get('milestone'):
            raise serializers.ValidationError("Either 'post' or 'milestone' must be provided.")
        if data.get('post') and data.get('milestone'):
            raise serializers.ValidationError("Only one of 'post' or 'milestone' can be provided.")
        return data

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })