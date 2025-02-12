import time

from celery import shared_task

@shared_task
def my_task(arg1, arg2):
    # Task logic here
    time.sleep(5)
    result = arg1 + arg2
    return result



@shared_task
def periodic_task():
    return "iam a perodic task"