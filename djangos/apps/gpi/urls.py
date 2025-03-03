from django.urls import path, include
from rest_framework import routers
from .views_list.libitemviewset  import LibitemViewSet
from .views_list.sysmenuviewset import SysmenuViewSet
from .views_list.fileuploadview import FileUploadViewSet
router = routers.DefaultRouter()
router.register('Libitem', LibitemViewSet, basename="Libitem")
router.register('Sysmenu', SysmenuViewSet, basename="Sysmenu")
router.register('File', FileUploadViewSet, basename="File")
urlpatterns = [
    path('', include(router.urls)),
]
