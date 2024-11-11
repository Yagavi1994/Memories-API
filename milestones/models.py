from django.db import models
from django.contrib.auth.models import User

class Milestone(models.Model):
    CATEGORY_CHOICES = [
        ('physical', 'Physical'),
        ('cognitive', 'Cognitive'),
        ('emotional', 'Emotional'),
        ('social', 'Social'),
        ('language', 'Language'),
        ('other', 'Other'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    milestone_date = models.DateField(blank=False)
    image = models.ImageField(
        upload_to="images/", default="images/default_milestone_tmodxy", blank=False
    )
    age_years = models.PositiveIntegerField(null=True, blank=True)
    age_months = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True, help_text="Height in cm")
    weight = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True, help_text="Weight in kg"
    ) 
    milestone_category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="Category of the milestone",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} {self.title}"
