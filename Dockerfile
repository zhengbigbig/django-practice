# 基础镜像
FROM python:3.7-alpine
MAINTAINER zbb
# 设置镜像源
RUN pip install -U pip
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
#RUN apk add --no-cache jpeg-dev zlib-dev
#RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
#    && pip install Pillow
# 在容器内/var/www/html/下创建 mysite3文件夹
RUN mkdir -p /home/project
# 设置容器内工作目录
WORKDIR /home/project
# 将当前目录文件拷贝一份到工作目录中（. 表示当前目录）
ADD . /home/project
# 利用 pip 安装依赖
RUN pip install -r requirement.txt
RUN pip install uwsgi
EXPOSE 8080
# 设置start.sh文件可执行权限
RUN chmod +x ./start.sh
ENTRYPOINT ["./start.sh"]
