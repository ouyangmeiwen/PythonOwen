# 使用 Python 官方基础镜像
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖，包括 mysqlclient 所需要的 MySQL 库
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# 复制 requirements.txt 文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 安装 Gunicorn
RUN pip3 install gunicorn

# 暴露 Django 默认端口
EXPOSE 9001

# 使用 Gunicorn 启动 Django 应用
CMD ["gunicorn", "djapps.wsgi:application", "--bind", "0.0.0.0:9001", "--workers", "4"]