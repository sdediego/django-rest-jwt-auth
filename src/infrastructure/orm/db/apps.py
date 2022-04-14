# coding: utf-8

from django.apps import AppConfig


class ExchangeRateConfig(AppConfig):
    label = 'account'
    name = 'src.infrastructure.orm.db.account'
    verbose_name = 'Account'
