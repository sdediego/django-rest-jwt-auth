# coding: utf-8

from http import HTTPStatus
from unittest.mock import Mock

from django.test.client import RequestFactory

import pytest

from src.infrastructure.api.views.account import UserViewSet
from tests.fixtures import token, user


@pytest.mark.unit
def test_user_viewset_login(token):
    request = RequestFactory()
    request.data = Mock()
    viewset = UserViewSet()
    viewset.viewset_factory = Mock()
    mock_factory_create = viewset.viewset_factory.create
    mock_factory_create.return_value = Mock()
    mock_controller_login = mock_factory_create.return_value.login
    mock_controller_login.return_value = (vars(token), HTTPStatus.OK.value)
    response = viewset.login(request)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)


@pytest.mark.unit
def test_user_viewset_refresh(token):
    request = RequestFactory()
    request.headers = {
        'Authorization': token.token
    }
    viewset = UserViewSet()
    viewset.viewset_factory = Mock()
    mock_factory_create = viewset.viewset_factory.create
    mock_factory_create.return_value = Mock()
    mock_controller_refresh = mock_factory_create.return_value.refresh
    mock_controller_refresh.return_value = (vars(token), HTTPStatus.OK.value)
    response = viewset.refresh(request)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)


@pytest.mark.unit
def test_user_viewset_register(user):
    request = RequestFactory()
    request.data = Mock()
    viewset = UserViewSet()
    viewset.viewset_factory = Mock()
    mock_factory_create = viewset.viewset_factory.create
    mock_factory_create.return_value = Mock()
    mock_controller_register = mock_factory_create.return_value.register
    mock_controller_register.return_value = (vars(user), HTTPStatus.CREATED.value)
    response = viewset.register(request)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.CREATED.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
