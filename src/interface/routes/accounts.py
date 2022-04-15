# coding: utf-8

from src.domain.core.constants import HTTP_VERB_POST
from src.domain.core.routing import Route, Router
from src.interface.controllers.account import UserController


user_router = Router()
user_router.register({
    Route(
        http_verb=HTTP_VERB_POST,
        path=r'^accounts/users/register/$',
        controller=UserController,
        method='post',
        name='user_register'
    )
})
