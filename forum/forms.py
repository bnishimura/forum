from django import forms
from .models import Thread, Post


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        # remove author later
        fields = ['title', 'body', 'author']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # remove author later
        fields = ['body', 'author']
