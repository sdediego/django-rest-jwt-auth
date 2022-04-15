# coding: utf-8

from http import HTTPStatus
from unittest.mock import Mock

from django.test.client import RequestFactory

import pytest

from src.infrastructure.api.views.account import UserViewSet
from tests.fixtures import user


@pytest.mark.unit
def test_user_viewset_register(user):
    request = RequestFactory()
    request.data = Mock()
    viewset = UserViewSet()
    viewset.viewset_factory = Mock()
    mock_factory_create = viewset.viewset_factory.create
    mock_factory_create.return_value = Mock()
    mock_controller_register = mock_factory_create.return_value.register
    mock_controller_register.return_value = (vars(user), HTTPStatus.OK.value)
    response = viewset.register(request)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
