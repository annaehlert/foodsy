from django.utils import timezone
from django.db import models

CATEGORY = (
    ("lunch", "lunch"),
    ("śniadanie", "śniadanie"),
    ("obiad", "obiad"),
    ("kolacja", "kolacja"),
    ("deser", "deser"),
    ("wegetariańskie", "wegetariańskie"),
    ("szybkie", "szybkie"),
    ("mięsne", "mięsne"),
    ("proste", "proste"),
)


class Profile(models.Model):
    user_id = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True, related_name="user")
    avatar = models.ImageField(upload_to='media', default='default.jpg')


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="post")
    image = models.ImageField(blank=True, null=True, verbose_name="zdjęcie")
    description = models.CharField(max_length=255, verbose_name="nazwa przepisu")
    recipe = models.TextField(verbose_name="przepis")
    date = models.DateTimeField(default=timezone.now)
    # category = models.TextField(choices=CATEGORY, max_length=20, null=True)

    def __str__(self):
        return self.author.user_id.username


class Follower(models.Model):
    user = models.OneToOneField(Profile, related_name="followers", on_delete=models.CASCADE)
    follower_user = models.ManyToManyField(Profile, related_name='follower_user')


class Following(models.Model):
    user = models.OneToOneField(Profile, related_name="following", on_delete=models.CASCADE)
    following_user = models.ManyToManyField(Profile, related_name='following_user')


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="użytkownik")
    content = models.TextField(default=" ", verbose_name="treść")
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Category(models.Model):
    category = models.CharField(choices=CATEGORY, verbose_name="kategoria", max_length=20, null=True)
    post = models.ManyToManyField(Post, related_name="category")

