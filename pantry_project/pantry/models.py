from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    # Links UserProfile to a Django User model instance
    # Model already includes user_id, username, and password fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional fields
    bio = models.CharField(max_length=200)
    photoURL = models.ImageField(upload_to="", blank=True)
