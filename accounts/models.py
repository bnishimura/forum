from django.db import models
from django.contrib.auth.models import User


class ForumUser(User):

    post_count = models.PositiveIntegerField()

    REQUIRED_FIELDS = []

    # user associated media (avatar, etc)
