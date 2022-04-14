from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from accounts.models import ForumUser


def get_sentinel_user():
    return get_user_model().objects.get_or_create(
            name="deleted")[0]

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

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.SET(get_sentinel_user)
            )
    subforum = models.ForeignKey(Subforum,
            on_delete = models.CASCADE)
    body = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(title)
        return super(Thread, self).save(*args, **kwargs)

#    def get_absolute_url(self):
#        return reverse('thread', args=[self.subforum, self.pk])

class Post(models.Model):
    # posts by deleted users will not be deleted. 
    # Instead, it shows a generic user
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user)
        )
    thread = models.ForeignKey(Thread,
        on_delete = models.CASCADE,
        null=True)
    body = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', 
            on_delete=models.DO_NOTHING,
            null=True)

    def __str(self):
        return self.title

#    def get_absolute_url(self):
#        return reverse('thread', 
#                args=[self.thread.subforum, self.thread.slug])
