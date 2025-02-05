# views.py
from django.http import JsonResponse
from fastapi import openapi
from fastapi.responses import FileResponse
from ..model_list.libitem import (Libitem)
from ..serializers_list.uploadedfileserializer import UploadedFileSerializer,DownloadFileSerializer  # 假设我们使用 DRF 序列化器
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import os
from django.conf import settings
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import mimetypes
from urllib.parse import quote
from django.http import StreamingHttpResponse

class FileUploadViewSet(ModelViewSet):
    queryset = Libitem.objects.all()
    serializer_class = UploadedFileSerializer
    pagination_class = None
    ordering_fields = ['pk']
    ordering = ['pk']
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)  # 支持多部分数据上传

    def get_serializer_class(self):
        if self.action == 'upload_file':
            return UploadedFileSerializer
        elif self.action == 'download_file':
            return DownloadFileSerializer
    
    #def create(self, request, *args, **kwargs):
    @action(methods=['post'],detail=False,url_name='upload_file')
    def upload_file(self, request, *args, **kwargs):
        file_serializer = self.get_serializer(data=request.data)
        if file_serializer.is_valid():
            file_obj = file_serializer.validated_data['file']
            
            # 定义文件保存路径
            save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_obj.name)
            with open(save_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
            
            return JsonResponse({"message": "File uploaded successfully!", "file_path": save_path}, status=201)
        
        return JsonResponse(file_serializer.errors, status=400)


    @swagger_auto_schema(query_serializer=DownloadFileSerializer)
    @action(methods=['get'], detail=False, url_name='download_file')
    def download_file(self, request, *args, **kwargs):
        """
        提供文件下载功能
        - Query Parameter: file_name (要下载的文件名)
        """
        file_name = request.query_params.get('file_name')
        if not file_name:
            return JsonResponse({"error": "file_name parameter is required."}, status=400)
        
        # 文件路径
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)
        
        if not os.path.exists(file_path):
            return JsonResponse({"error": "File not found."}, status=404)
        
         # 使用 StreamingHttpResponse 来流式传输文件
        def file_iterator(file_path, chunk_size=1024*8):
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    yield chunk
        response = StreamingHttpResponse(file_iterator(file_path), content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
        return response
           