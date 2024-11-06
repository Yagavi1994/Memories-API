from django.db import models
from django.contrib.auth.models import User
from PIL import Image  # Import Pillow for image processing

class Profile(models.Model):
    """
    Profile model for user profiles.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default-profile.jpg')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            # Make the image square by cropping or resizing
            min_dimension = min(img.size)
            left = (img.width - min_dimension) / 2
            top = (img.height - min_dimension) / 2
            right = (img.width + min_dimension) / 2
            bottom = (img.height + min_dimension) / 2

            img = img.crop((left, top, right, bottom))
            img = img.resize((min_dimension, min_dimension), Image.ANTIALIAS)
            img.save(self.image.path)

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)
