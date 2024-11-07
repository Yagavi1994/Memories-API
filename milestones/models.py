from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Milestone(models.Model):
    """
    Milestone model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    milestone_date = models.DateField(blank=False)
    image = models.ImageField(
        upload_to="images/", default="images/default_milestone_tmodxy", blank=False
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} {self.title}"