from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    photo = CloudinaryField('image', blank=True)

    def set_default_photo(sender, instance, created, **kwargs):
        if created and not instance.photo:
            instance.photo = '/media/avatar.jpeg'
            instance.save()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = CloudinaryField('image', blank=True)
    description = models.TextField()

    def __str__(self):
        return self.description


class Tag(models.Model):
    name = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Follower(models.Model):
    follower_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)


class Like(models.Model):
    person_id = models.ForeignKey(User, related_name="user_likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="liked_post", on_delete=models.CASCADE)
