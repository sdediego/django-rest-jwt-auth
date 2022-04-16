# coding: utf-8

from http import HTTPStatus
from unittest.mock import Mock

import pytest

from src.interface.controllers.account import UserController
from src.domain.exceptions import EntityDuplicate
from tests.fixtures import user


@pytest.mark.unit
def test_user_controller_register(user):
    params = {
        'email': user.email,
        'password': user.password,
        'password2': user.password
    }
    user_interator = Mock()
    user_interator.register.return_value = user
    controller = UserController(user_interator)
    data, status = controller.register(params)
    assert user_interator.register.called
    assert status == HTTPStatus.CREATED.value
    assert data['email'] == user.email


@pytest.mark.unit
def test_user_controller_register_bad_request(user):
    params = {
        'email': user.email,
        'password': user.password
    }
    user_interator = Mock()
    user_interator.register.return_value = user
    controller = UserController(user_interator)
    data, status = controller.register(params)
    assert not user_interator.register.called
    assert status == HTTPStatus.BAD_REQUEST.value
    assert 'errors' in data


@pytest.mark.unit
def test_user_controller_register_duplicate(user):
    params = {
        'email': user.email,
        'password': user.password,
        'password2': user.password
    }
    error_message = 'Already exists a user with this data'
    user_interator = Mock()
    user_interator.register.side_effect = EntityDuplicate(error_message)
    controller = UserController(user_interator)
    data, status = controller.register(params)
    assert user_interator.register.called
    assert status == HTTPStatus.BAD_REQUEST.value
    assert 'error' in data
    assert error_message in data['error']
