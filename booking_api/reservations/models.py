from django.db import models

from users.models import User


class Reservation(models.Model):
    date = models.DateField(
        verbose_name="Дата",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    gender = models.CharField(
        verbose_name="Мужской или женский разряд",
        max_length=30,
    )
    floor = models.IntegerField(verbose_name="Этаж. 2 или 3")
    start_hour = models.IntegerField(verbose_name="Начало в")
    finish_hour = models.IntegerField(verbose_name="Конец в")
    cost = models.IntegerField(
        verbose_name="Цена бронирования",
    )
    confirmed = models.BooleanField(default=False)
    payment_type = models.CharField(
        verbose_name="Оплачено наличными или картой",
        max_length=15,
        null=True,
        default=None,
    )
