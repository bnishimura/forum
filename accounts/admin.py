from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ForumUser
from .forms import AdminCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = AdminCreationForm
    model = ForumUser

admin.site.register(ForumUser, CustomUserAdmin)
