#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# # 确保当前工作目录是脚本所在目录  保证可以从上级启动
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djapi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv)<=1:
        sys.argv=['manage.py', 'runserver', '9001']
    execute_from_command_line(sys.argv)
    print("http://127.0.0.1:9001/api/swagger/")  #如果无法打开请注意将VSCode目录调整为当前程序的根目录

if __name__ == '__main__':
    main()
