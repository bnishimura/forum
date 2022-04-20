from django.contrib import admin
from django import forms
from .models import Category, Subforum, Post, Thread


class SubforumAdmin(admin.ModelAdmin):
    model = Subforum
    fields = ('title', 'description', 'category')

admin.site.register(Category)
admin.site.register(Subforum, SubforumAdmin)
admin.site.register(Post)
admin.site.register(Thread)
