@echo off
REM 激活虚拟环境
call %~dp0venv\Scripts\activate

REM 切换到批处理文件所在目录
cd /d %~dp0

REM 
#python manage.py runserver 9001