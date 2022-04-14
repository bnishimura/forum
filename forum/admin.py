from django.contrib import admin
from .models import Category, Subforum, Post, Thread


class ThreadAdmin(admin.ModelAdmin):
    propopulated_fields = {"slug": ("title",)}
    

admin.site.register(Category)
admin.site.register(Subforum)
admin.site.register(Post)
admin.site.register(Thread)
