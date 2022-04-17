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

    def login(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        payload, status = self.controller.login(data)
        return Response(data=payload, status=status)

    def refresh(self, request: Request, *args, **kwargs) -> Response:
        token = request.headers.get('Authorization', '')
        payload, status = self.controller.refresh(token=token)
        return Response(data=payload, status=status)

    def register(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        payload, status = self.controller.register(data)
        return Response(data=payload, status=status)
    