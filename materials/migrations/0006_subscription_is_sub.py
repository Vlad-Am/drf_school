# Generated by Django 5.0.4 on 2024-05-06 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0005_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="is_sub",
            field=models.BooleanField(default=False, verbose_name="подписка"),
        ),
    ]
