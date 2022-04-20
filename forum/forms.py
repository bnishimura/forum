from django import forms
from .models import Thread, Post, Subforum


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'body']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']

class SubforumForm(forms.ModelForm):
    class Meta:
        model = Subforum
        fields = ['title', 'description', 'category']
