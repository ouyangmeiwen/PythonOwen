from django.apps import AppConfig


class GpiConfig(AppConfig):
    name = 'apps.gpi'
    verbose_name = 'gpi接口'
    
    def ready(self):
       print('开始执行gpi')