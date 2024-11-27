from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from milestones.models import Milestone


class Like(models.Model):
    """
    Like model, related to 'owner' and 'post' or 'milestone'.
    'owner' is a User instance, 'post' is a Post instance, and 'milestone'
    is a Milestone instance.
    'unique_together' ensures a user can't like the same post or milestone
    twice.
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    milestone = models.ForeignKey(
        Milestone,
        related_name='likes',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'post'], name='unique_like_post'
            ),
            models.UniqueConstraint(
                fields=['owner', 'milestone'], name='unique_like_milestone'
            )
        ]

    def __str__(self):
        return f'{self.owner} {self.post or self.milestone}'  # noqa
