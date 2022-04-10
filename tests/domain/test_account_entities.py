# coding: utf-8

from datetime import datetime

import pytest

from src.domain.account import UserEntity
from tests.fixtures import user


@pytest.mark.unit
def test_user_entity_attrs(user):
    assert isinstance(user.name, str)
    assert isinstance(user.surname, str)
    assert isinstance(user.username, str)
    assert isinstance(user.email, str)
    assert isinstance(user.password, str)
    assert isinstance(user.is_active, bool)
    assert isinstance(user.name, str)
    assert isinstance(user.last_login, str)
    assert isinstance(user.date_joined, str)


@pytest.mark.unit
def test_user_entity_post_init(user):
    now = datetime.now()
    new_user = UserEntity(
        name=user.name,
        surname=user.surname,
        username=user.username,
        email=user.email,
        password=user.password,
        is_active=user.is_active,
        last_login=now,
        date_joined=now
    )
    assert new_user.last_login == now.strftime('%Y-%m-%d %H:%M:%S')
    assert new_user.date_joined == now.strftime('%Y-%m-%d %H:%M:%S')


@pytest.mark.unit
def test_user_entity_representation(user):
    user_str = UserEntity.to_string(user)
    assert isinstance(user_str, str)
    assert user.email in user_str
    assert user.username in user_str
    user.username = None
    user_str = UserEntity.to_string(user)
    assert user.email == user_str


@pytest.mark.unit
def test_user_entity_full_name_property(user):
    assert isinstance(user.full_name, str)
    assert user.full_name == f'{user.name} {user.surname}'
