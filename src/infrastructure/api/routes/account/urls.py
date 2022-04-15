# coding: utf-8

from django.conf.urls import include
from django.urls import path

from src.infrastructure.api.routes.account.routers import UserRouter
from src.infrastructure.api.views.account import UserViewSet


user_router = UserRouter()
user_router.register('', viewset=UserViewSet, basename='accounts')


urlpatterns = [
    path('', include(user_router.urls))
]
