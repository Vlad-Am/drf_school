import json
from datetime import datetime, timedelta

from django_celery_beat.models import IntervalSchedule, PeriodicTask

schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)
PeriodicTask.objects.create(
    interval=schedule,                  # we created this above.
    name='Importing contacts',          # simply describes this periodic task.
    task='materials.tasks.set_is_active_for_user',  # name of task.
    args=json.dumps(['arg1', 'arg2']),
    kwargs=json.dumps({
       'be_careful': True,
    }),
    expires=datetime.now() + timedelta(seconds=30)
)
