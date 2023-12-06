from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdBy")
    likes = models.ManyToManyField(User, blank=True, related_name="likedBy")
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

class UserNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
