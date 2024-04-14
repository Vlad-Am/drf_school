from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(max_length=35, verbose_name="phone number", **NULLABLE)
    avatar = models.ImageField(upload_to="media/", verbose_name="avatar", **NULLABLE)
    token = models.CharField(max_length=100, verbose_name="token", **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name="is_active")
    city = models.CharField(max_length=50, verbose_name="city", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("set_is_activated", "Может блокировать пользователя")]


# class Pays(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     date = models.DateField()
