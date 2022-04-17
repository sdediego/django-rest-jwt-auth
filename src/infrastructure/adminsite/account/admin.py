# coding: utf-8

from django.contrib import admin

from src.infrastructure.orm.db.account.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'full_name', 'username', 'email', 'is_active', 'last_login')
    readonly_fields = ('password', 'last_login', 'date_joined')
    ordering = ('email', 'username')
