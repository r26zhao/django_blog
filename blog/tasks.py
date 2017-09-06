from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time


@shared_task
def send_mail(email):
    print('sending email...')
    time.sleep(2)
    print('finished')
    return True