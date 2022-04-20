from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
#from accounts.models import ForumUser


def get_sentinel_user():
    # can anyone login this deleted user?
    return get_user_model().objects.get_or_create(
            username="[deleted]")[0]

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subforum(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    # deleted categories delete all subfora within
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    path = models.SlugField(max_length=50, null=True)

    def save(self, *args, **kwargs):
        self.path = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE
            )
    subforum = models.ForeignKey(Subforum,
            on_delete = models.CASCADE)
    body = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

class Post(models.Model):
    # posts by deleted users will not be deleted. 
    # Instead, it shows a generic user
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    thread = models.ForeignKey(Thread,
        on_delete = models.CASCADE,
        null=True)
    body = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    repliesTo = models.ForeignKey('self', 
            on_delete=models.CASCADE,
            null=True)

    def __str(self):
        return self.title
