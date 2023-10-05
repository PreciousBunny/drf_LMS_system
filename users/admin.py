from django.contrib import admin
from .models import User


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'city', 'is_active', 'role',)
    list_filter = ('id', 'is_active', 'role',)
