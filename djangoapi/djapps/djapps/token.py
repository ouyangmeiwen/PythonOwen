from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import *


class CusTokenObtainPairView(TokenObtainPairView):
    # 自定义 token 获取
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
         # 获取返回的原始数据
        data = response.data
        # 自定义 JSON 响应
        return JsonResponse({
            'message': 'Token obtained successfully',
            'access_token': data['access'],
            'refresh_token': data['refresh'],
            #'user': request.user.username,  # 如果需要额外返回用户信息
        })


class CusTokenRefreshView(TokenRefreshView):
    # 自定义 token 刷新
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # 获取返回的原始数据
        data = response.data
        # 自定义 JSON 响应
        return JsonResponse({
            'message': 'Token refreshed successfully',
            'access_token': data['access'],
        })
