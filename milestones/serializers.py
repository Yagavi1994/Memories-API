from rest_framework import serializers
from .models import Milestone
from likes.models import Like

class MilestoneSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(
        source="owner.profile.image.url"
    )
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    milestone_category_display = serializers.SerializerMethodField()

    age_years = serializers.IntegerField(required=False, allow_null=True)
    age_months = serializers.IntegerField(required=False, allow_null=True)
    height = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    milestone_date = serializers.DateField(required=False, allow_null=True)  # Optional field
    content = serializers.CharField(required=False, allow_blank=True)  # Optional field

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size larger than 2MB!")
        if value.image.height > 4096:
            raise serializers.ValidationError("Image height larger than 4096px!")
        if value.image.width > 4096:
            raise serializers.ValidationError("Image width larger than 4096px!")
        return value

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, milestone=obj
            ).first()
            return like.id if like else None
        return None

    def get_milestone_category_display(self, obj):
        # Display the label for the milestone category field
        return obj.get_milestone_category_display()

    class Meta:
        model = Milestone
        fields = [
            "id",
            "owner",
            "is_owner",
            "profile_id",
            "profile_image",
            "created_at",
            "updated_at",
            "title",
            "content",
            "milestone_date",
            "image",
            "like_id", 
            "likes_count", 
            "comments_count",
            "age_years", 
            "age_months",
            "height", 
            "weight", 
            "milestone_category",
            "milestone_category_display",
        ]
