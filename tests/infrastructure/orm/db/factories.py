# coding: utf-8

import string
from datetime import datetime, timezone

from factory import django, fuzzy

from src.infrastructure.orm.db.account.models import User


class UserFactory(django.DjangoModelFactory):

    class Meta:
        model = User

    name = fuzzy.FuzzyText(length=20, chars=string.ascii_letters)
    surname = fuzzy.FuzzyText(length=20, chars=string.ascii_letters)
    username = fuzzy.FuzzyText(length=20, chars=string.ascii_letters)
    email = fuzzy.FuzzyText(length=20, chars=string.ascii_letters, suffix='@mail.com')
    password = fuzzy.FuzzyText(length=20, prefix='Password_1234')
    is_active = fuzzy.FuzzyChoice([True, False])
    last_login = fuzzy.FuzzyDateTime(start_dt=datetime.now(tz=timezone.utc))
    date_joined = fuzzy.FuzzyDateTime(start_dt=datetime.now(tz=timezone.utc))
