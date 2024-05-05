from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def my_send_email(recipient_list):
    """Определяем задачу my_task, которая будет выполняться
     периодически в соответствии с расписанием, установленным в настройках"""
    send_mail("Обновление", "We are updating", settings.EMAIL_HOST_USER, recipient_list)
