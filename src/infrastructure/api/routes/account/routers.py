# coding: utf-8

from rest_framework.routers import Route, SimpleRouter

from src.infrastructure.factories.account import UserViewSetFactory
from src.interface.routes.accounts import user_router


class UserRouter(SimpleRouter):
    routes = [
        Route(
            url=user_router.get_url('user_login'),
            mapping=user_router.map('user_login'),
            initkwargs={'viewset_factory': UserViewSetFactory},
            name='{basename}-login',
            detail=False
        ),
        Route(
            url=user_router.get_url('user_register'),
            mapping=user_router.map('user_register'),
            initkwargs={'viewset_factory': UserViewSetFactory},
            name='{basename}-register',
            detail=False
        ),
        Route(
            url=user_router.get_url('token_refresh'),
            mapping=user_router.map('token_refresh'),
            initkwargs={'viewset_factory': UserViewSetFactory},
            name='{basename}-refresh',
            detail=False
        )
    ]
