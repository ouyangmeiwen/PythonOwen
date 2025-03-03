from django.urls import path,include
from .views_list.hello_view import hello
from .views_list.libitem_view import *
from rest_framework.routers import DefaultRouter
from .views_list.libitemviewset import LibitemViewSet
from .views_list.sysmenuviewset import SysmenuViewSet



router = DefaultRouter()
router.register(r'libitems', LibitemViewSet, basename='libitems')
router.register(r'sysmenu', SysmenuViewSet, basename='sysmenu')
urlpatterns = [
     # JWT Token 获取接口
    path('', include(router.urls)),
    path('hello', hello),
    path('libitem', LibItemView.as_view(), name='libitem'),
]