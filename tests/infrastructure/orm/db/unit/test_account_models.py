# coding: utf-8

import dataclasses

import pytest

from src.domain.entities.account import UserEntity
from src.infrastructure.orm.db.account.models import User
from tests.fixtures import user


def create_user_model(user) -> User:
    return User(**dataclasses.asdict(user))


@pytest.mark.unit
def test_user_attrs(user):
    model = create_user_model(user)
    assert isinstance(model, User)
    assert isinstance(model.name, str)
    assert isinstance(model.surname, str)
    assert isinstance(model.username, str)
    assert isinstance(model.email, str)
    assert isinstance(model.password, str)
    assert isinstance(model.is_active, bool)
    assert isinstance(model.last_login, str)
    assert isinstance(model.date_joined, str)


@pytest.mark.unit
def test_user_representation(user):
    model = create_user_model(user)
    assert str(model) == str(user)


@pytest.mark.unit
def test_user_map(user):
    model = create_user_model(user)
    assert isinstance(model.map(), UserEntity)


@pytest.mark.unit
def test_user_full_name(user):
    model = create_user_model(user)
    assert model.full_name == user.full_name
