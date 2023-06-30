from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post_photo/')
    description = models.TextField()

    def __str__(self):
        return self.description


class Tag(models.Model):
    name = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
