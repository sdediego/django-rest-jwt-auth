# coding: utf-8

from datetime import datetime

import pytest

from src.domain.account import UserEntity, UserTokenEntity
from tests.fixtures import user, user_token


@pytest.mark.unit
def test_user_entity_attrs(user):
    assert isinstance(user.id, int)
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
def test_user_entity_post_init():
    now = datetime.now()
    new_user = UserEntity(last_login=now, date_joined=now)
    assert new_user.last_login == now.strftime('%Y-%m-%d %H:%M:%S')
    assert new_user.date_joined == now.strftime('%Y-%m-%d %H:%M:%S')


@pytest.mark.unit
def test_user_entity_representation(user):
    user_str = UserEntity.to_string(user)
    assert isinstance(user_str, str)
    assert str(user.id) in user_str
    assert user.email in user_str
    assert user.username in user_str
    user.username = None
    user_str = UserEntity.to_string(user)
    assert f'User {str(user.id)}: {user.email}' == user_str


@pytest.mark.unit
def test_user_entity_full_name_property(user):
    assert isinstance(user.full_name, str)
    assert user.full_name == f'{user.name} {user.surname}'


@pytest.mark.unit
def test_user_token_entity_attrs(user_token):
    assert isinstance(user_token.user, UserEntity)
    assert isinstance(user_token.token, str)


@pytest.mark.unit
def test_user_token_entity_representation(user_token):
    user_token_str = UserTokenEntity.to_string(user_token)
    assert isinstance(user_token_str, str)
    assert str(user_token.user) in user_token_str
    assert user_token.token in user_token_str
