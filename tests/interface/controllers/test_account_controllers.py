# coding: utf-8

from http import HTTPStatus
from unittest.mock import Mock

import pytest

from src.interface.controllers.account import UserController
from src.domain.exceptions import EntityDoesNotExist, EntityDuplicate
from tests.fixtures import token, user


@pytest.mark.unit
def test_user_controller_login(user):
    params = {
        'email': user.email,
        'password': user.password
    }
    user_interator = Mock()
    user_interator.login.return_value = user
    controller = UserController(user_interator)
    data, status = controller.login(params)
    assert user_interator.login.called
    assert status == HTTPStatus.OK.value
    assert 'token' in data


@pytest.mark.unit
def test_user_controller_login_bad_request(user):
    params = {
        'email': user.email
    }
    user_interator = Mock()
    user_interator.login.return_value = user
    controller = UserController(user_interator)
    data, status = controller.login(params)
    assert not user_interator.login.called
    assert status == HTTPStatus.BAD_REQUEST.value
    assert 'errors' in data


@pytest.mark.unit
def test_user_controller_login_does_not_exist(user):
    params = {
        'email': user.email,
        'password': user.password
    }
    error_message = 'User does not exist with this data'
    user_interator = Mock()
    user_interator.login.side_effect = EntityDoesNotExist(error_message)
    controller = UserController(user_interator)
    data, status = controller.login(params)
    assert user_interator.login.called
    assert status == HTTPStatus.BAD_REQUEST.value
    assert 'error' in data
    assert error_message in data['error']


@pytest.mark.unit
def test_user_controller_refresh(token):
    user_interator = Mock()
    controller = UserController(user_interator)
    data, status = controller.refresh(token.token)
    assert status == HTTPStatus.OK.value
    assert 'token' in data


@pytest.mark.unit
def test_user_controller_refresh_bad_request():
    user_interator = Mock()
    controller = UserController(user_interator)
    invalid_token = 123456789
    data, status = controller.refresh(invalid_token)
    assert status == HTTPStatus.BAD_REQUEST.value
    assert 'errors' in data


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
