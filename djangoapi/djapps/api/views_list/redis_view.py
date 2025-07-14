from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import *
from rest_framework.views import APIView
from ..model_list.libitem import Libitem
from ..utils_lst.string_helper import convert_model_to_dict
from rest_framework.permissions import AllowAny
from django.core.cache import cache

class RedisView(APIView):
    authentication_classes = [JWTAuthentication]  # 使用 JWT 认证
    #permission_classes = [IsAuthenticated]       # 需要认证才能访问
    permission_classes = [AllowAny]       # 需要认证才能访问
    # curl http://127.0.0.1:9001/api/redis
    # http://127.0.0.1:9001/api/redis
    #curl -X GET http://127.0.0.1:9001/api/redis
    def get(self, request):
        """处理 GET 请求，获取 Redis 缓存"""
        value = cache.get("my_key")
        return JsonResponse({'value': value})

    #curl -X POST http://127.0.0.1:9001/api/redis -H "Content-Type: application/json" -d '{"key": "user123", "value": "John Doe", "timeout": 120}'
    def post(self, request):
        """处理 POST 请求，设置 Redis 缓存"""
        key = request.data.get("key", "default_key")
        value = request.data.get("value", "default_value")
        timeout = request.data.get("timeout", 60)  # 默认 60 秒
        cache.set(key, value, timeout=timeout)
        return JsonResponse({'message': f'Key "{key}" set to "{value}" with timeout {timeout} seconds'})

    #curl -X PUT http://127.0.0.1:9001/api/redis -H "Content-Type: application/json" -d '{"key": "user123", "value": "Jane Doe"}'
    def put(self, request):
        """处理 PUT 请求，更新 Redis 缓存"""
        key = request.data.get("key")
        value = request.data.get("value")
        if cache.get(key) is None:
            return JsonResponse({'error': 'Key does not exist'}, status=404)
        cache.set(key, value, timeout=60)  # 更新 60 秒
        return JsonResponse({'message': f'Key "{key}" updated to "{value}"'})

    #curl -X DELETE http://127.0.0.1:9001/api/redis -H "Content-Type: application/json" -d '{"key": "user123"}'
    def delete(self, request):
        """处理 DELETE 请求，删除 Redis 缓存"""
        key = request.data.get("key")
        if cache.get(key) is None:
            return JsonResponse({'error': 'Key does not exist'}, status=404)
        cache.delete(key)
        return JsonResponse({'message': f'Key "{key}" deleted'})

