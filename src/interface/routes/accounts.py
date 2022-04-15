# coding: utf-8

from src.domain.core.constants import HTTP_VERB_POST
from src.domain.core.routing import Route, Router
from src.interface.controllers.account import UserController


account_router = Router()
account_router.register({
    Route(
        http_verb=HTTP_VERB_POST,
        path=r'^accounts/register/$',
        controller=UserController,
        method='post',
        name='account_register'
    )
})
