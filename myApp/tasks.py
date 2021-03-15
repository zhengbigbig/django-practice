from celery import shared_task
from celery.signals import task_success
import time

from django.core.mail import send_mail
from django.conf import settings

@shared_task
def hello_celery(n):
    for i in range(n):
        print('hello')
        time.sleep(2)

# 异步发送邮件
@shared_task
def mail_send(mail):
    """
    subject,message,from_email,recipient_list
    :param mail: 字典 {'subject':'hello'}
    :return:
    """
    send_mail(**mail, from_email=settings.EMAIL_HOST_USER)


@shared_task
def sum_even(n):
    result = 0
    for i in (0, n + 1, 2):
        result += i
    return result


# 获取异步任务的结果
@task_success.connect(sender=sum_even)
def task_done_handler(sender=None, result=None, **kwargs):
    # 'after_task_publish for task id {body[id]}'.format(body=body)
    print('add -------')
    print(result)
