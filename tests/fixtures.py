# coding: utf-8

import random
import string
from datetime import datetime

import pytest

from src.domain.account import UserEntity, UserTokenEntity


def generate_random_string(length: int) -> str:
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])


def get_current_datetime() -> datetime:
    return datetime.now()


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
        last_login=get_current_datetime(),
        date_joined=get_current_datetime()
    )


@pytest.fixture
def user_token(user) -> UserTokenEntity:
    return UserTokenEntity(
        user=user,
        token=generate_random_string(64)
    )
