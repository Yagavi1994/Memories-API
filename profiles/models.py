from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Model to represent a user's profile.
    Each user automatically gets a profile upon creation.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/',
        default='images/Profile-pic_dxmgt2'
    )
    is_private = models.BooleanField(default=False)  # Privacy setting field

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a profile when a User instance is created.
    """
    if created:
        Profile.objects.create(owner=instance)


# Connect the create_profile signal to the User model's post_save signal.
post_save.connect(create_profile, sender=User)
