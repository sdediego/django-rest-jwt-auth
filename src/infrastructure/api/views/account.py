# coding: utf-8

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from src.interface.controllers.account import UserController


class UserViewSet(ViewSet):
    viewset_factory = None

    @property
    def controller(self) -> UserController:
        return self.viewset_factory.create()

    def register(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        payload, status = self.controller.register(data)
        return Response(data=payload, status=status)
    