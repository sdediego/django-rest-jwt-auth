# coding: utf-8

import random
import string
from datetime import datetime, timedelta

import pytest

from src.domain.entities.account import TokenEntity, UserEntity
from src.domain.services.account import encode_token


def generate_random_string(length: int) -> str:
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])


def get_datetime() -> datetime:
    return datetime.now() + timedelta(hours=-1)


@pytest.fixture
def user() -> UserEntity:
    return UserEntity(
        id=random.randint(1, 10),
        name=generate_random_string(10),
        surname=generate_random_string(10),
        username=generate_random_string(10),
        email='test@test.com',
        password='Password_1234',
        is_active=random.choice([True, False]),
        last_login=get_datetime(),
        date_joined=get_datetime()
    )


@pytest.fixture
def token(user) -> TokenEntity:
    return encode_token(user.id)
