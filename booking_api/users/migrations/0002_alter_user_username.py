# Generated by Django 5.0.6 on 2024-09-11 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                default=None,
                max_length=20,
                null=True,
                verbose_name="username в Телеграм",
            ),
        ),
    ]
