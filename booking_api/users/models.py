from django.db import models

# import os


class User(models.Model):
    telegram_id = models.IntegerField(
        verbose_name="Телеграм ID",
        unique=True,
        primary_key=True,
    )
    username = models.CharField(
        max_length=20, verbose_name="username в Телеграм", null=True, default=None
    )
    registered_since = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата регистрации",
    )
    points = models.IntegerField(
        verbose_name="Бонусные баллы",
        default=0,
    )
