#!/bin/bash
# 注意：前两个服务一定要在后台运行，即后面加个&，最后一个服务要以前台运行。
#否则，全部以前台运行的话，只有第一个服务会启动；全部以后台运行的话，当最后一个服务执行完成后，容器就退出了
python manage.py collectstatic --noinput &
python manage.py makemigrations &
python manage.py migrate &
# 启动worker
celery worker -A project -l info -f /tmp/celery.log &  #这里注意日志位置要写绝对路径
# 启动beat
uwsgi --ini /home/project/uwsgi.ini &
celery beat -A project -l info
exec "$@"