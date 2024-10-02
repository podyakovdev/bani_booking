# Generated by Django 5.0.6 on 2024-09-18 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0002_reservation_payment_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="gender",
            field=models.CharField(
                default="мужской",
                max_length=15,
                verbose_name="Мужской или женский разряд",
            ),
            preserve_default=False,
        ),
    ]
