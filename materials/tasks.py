import smtplib
from calendar import monthrange

import pytz
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from users.models import User
import json
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule


@shared_task
def my_send_email(subs_email_list):
    """Отправляет сообщения об обновлении на subs_email_list"""
    try:
        send_mail("Обновление", "We are updating", settings.EMAIL_HOST_USER, set(subs_email_list),
                  fail_silently=False)
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@shared_task
def set_is_active_for_user():
    """Проверка пользователей по дате последнего входа по полю last_login
    и, если пользователь не заходил более месяца, блокировать его с помощью флага
    is_active"""
    zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(zone)
    month = now.month
    year = now.year
    days_count = monthrange(year, month)
    expiration_date = now - timedelta(days=days_count[1])
    user_list = User.objects.filter(last_login__lte=expiration_date, is_active=True)
    user_list.update(is_active=False)

    # users_list = User.objects.filter(is_active=True).all()
    #
    # for user in users_list:
    #
    #     if user.last_login is not None and user.last_login < datetime.now() - timedelta(days=1):
    #         user.is_active = False
    #         user.save()
