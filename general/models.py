from django.utils import timezone
from django.db import models


class Profile(models.Model):
    user_id = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True, related_name="user")
    avatar = models.ImageField(upload_to='media', default='default.jpg')

class Category(models.Model):
    category = models.CharField(verbose_name="kategoria", max_length=20, null=True)


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="post")
    image = models.ImageField(blank=True, null=True, verbose_name="zdjęcie")
    description = models.CharField(max_length=255, verbose_name="nazwa przepisu")
    recipe = models.TextField(verbose_name="przepis")
    date = models.DateTimeField(default=timezone.now)
    category = models.ManyToManyField(Category, related_name="categories", verbose_name="kategoria")

    def __str__(self):
        return self.author.user_id.username


class Follower(models.Model):
    user = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)
    follower_user = models.ForeignKey(Profile, related_name='follower_user', on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="użytkownik")
    content = models.TextField(default=" ", verbose_name="komentarz")
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Rewrite(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")


