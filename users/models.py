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


class Pays(models.Model):
    payment_method_choices = [
        ("card", "Карта"),
        ("cash", "Наличные"),
        ("transfer", "Перевод"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    amount = models.IntegerField(verbose_name="сумма оплаты", **NULLABLE)
    date = models.DateField(auto_now=True, verbose_name="дата оплаты", **NULLABLE)
    course = models.ForeignKey("materials.Course", on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE)
    payment_method = models.CharField(max_length=100, choices=payment_method_choices,
                                      verbose_name="Способ оплаты", **NULLABLE)
