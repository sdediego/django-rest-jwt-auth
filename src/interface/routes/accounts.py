# coding: utf-8

from src.interface.controllers.account import UserController
from src.interface.routes.core.constants import HTTP_VERB_GET, HTTP_VERB_POST
from src.interface.routes.core.routing import Route, Router


user_router = Router()
user_router.register([
    Route(
        http_verb=HTTP_VERB_POST,
        path=r'^accounts/users/login/$',
        controller=UserController,
        method='login',
        name='user_login'
    ),
    Route(
        http_verb=HTTP_VERB_POST,
        path=r'^accounts/users/register/$',
        controller=UserController,
        method='register',
        name='user_register'
    ),
    Route(
        http_verb=HTTP_VERB_GET,
        path=r'^accounts/users/token/refresh/$',
        controller=UserController,
        method='refresh',
        name='token_refresh'
    )
])
