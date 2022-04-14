from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ForumUser


class AdminCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = ForumUser
        fields = ('username', 'password')
