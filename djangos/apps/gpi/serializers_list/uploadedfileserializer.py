# serializers_list/uploadedfileserializer.py
from rest_framework import serializers
from django.core.exceptions import ValidationError


class UploadedFileSerializer(serializers.Serializer):
    file = serializers.FileField()  # 定义文件字段


    def validate_file(self, value):
        # 允许的文件扩展名和 MIME 类型
        allowed_extensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.txt']
        allowed_types = [
            'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel', 'text/plain'
        ]

        # 检查文件扩展名
        file_extension = '.' + value.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            raise ValidationError(f"Only document files are allowed. Allowed extensions: {', '.join(allowed_extensions)}")

        # 检查文件 MIME 类型
        if value.content_type not in allowed_types:
            raise ValidationError(f"Only document files are allowed. Allowed types: {', '.join(allowed_types)}")
        
        return value
    
class DownloadFileSerializer(serializers.Serializer):
    file_name=serializers.CharField(required=True,allow_null=False)