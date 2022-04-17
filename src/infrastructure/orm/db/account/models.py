# coding: utf-8

from typing import List

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.domain.entities.account import UserEntity


class User(models.Model):
    name = models.CharField(_('name'), max_length=100, blank=True)
    surname = models.CharField(_('surname'), max_length=100, blank=True)
    username = models.CharField(_('username'), max_length=20, blank=True, unique=True)
    email = models.EmailField(_('email'), db_index=True, unique=True)
    password = models.CharField(_('password'), max_length=64, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    last_login = models.DateTimeField(_('last login'), default=timezone.now)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('email',)

    def __str__(self) -> str:
        return str(self.map())

    def map(self, fields: List[str] = None) -> UserEntity:
        fields = fields or [str(field) for field in UserEntity.__dataclass_fields__]
        attrs = {field: getattr(self, field) for field in fields}
        return UserEntity(**attrs)

    @property
    def full_name(self) -> str:
        return self.map(fields=['name', 'surname']).full_name
