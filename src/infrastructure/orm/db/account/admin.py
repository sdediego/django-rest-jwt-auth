# coding: utf-8

from django.contrib import admin

from src.infrastructure.adminsite.account.admin import UserAdmin
from src.infrastructure.orm.db.account.models import User


admin.site.register(User, UserAdmin)
