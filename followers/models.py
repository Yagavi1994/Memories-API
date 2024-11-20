from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Follower(models.Model):
    """
    Follower model, related to 'owner' and 'followed'.
    'owner' is a User who is following another User.
    'followed' is a User being followed by 'owner'.
    """
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name='followed', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['owner', 'followed'], name='unique_follower')
        ]
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'

    def clean(self):
        if self.owner == self.followed:
            raise ValidationError("You cannot follow yourself.")
        super().clean()

    def __str__(self):
        return f"{self.owner.username} follows {self.followed.username}"
