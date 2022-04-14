# coding: utf-8

from django.contrib import admin

from src.infrastructure.orm.db.account.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('full_name', 'username', 'email', 'is_active', 'last_login')
    ordering = ('email', 'username')
