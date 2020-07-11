from django.utils import timezone
from django.db import models


class Users(models.Model):
    user_id = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media', default='media/default.jpg', null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    description = models.CharField(max_length=255)
    recipe = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class Follower(models.Model):
    user = models.OneToOneField(Users, related_name="followers", on_delete=models.CASCADE)
    follower_user = models.ManyToManyField(Users, related_name='follower_user')


class Following(models.Model):
    user = models.OneToOneField(Users, related_name="following", on_delete=models.CASCADE)
    following_user = models.ManyToManyField(Users, related_name='following_user')


class Comment(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField(default=" ")
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)