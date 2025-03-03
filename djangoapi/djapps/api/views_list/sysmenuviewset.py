import logging
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import *


from ..utils_lst import string_helper

from ..model_list.sysmenu import Sysmenu
from ..serializers_list.sysmenuserializer import SysmenuSerializer,QueryMenusInput



stringhelperinstancet=string_helper.StringHelper()
logger = logging.getLogger('log')

class SysmenuViewSet(ModelViewSet):
    queryset = Sysmenu.objects.all()
    serializer_class = SysmenuSerializer
    pagination_class = None  #默认开启分页
    ordering_fields = ['pk']
    ordering = ['pk']
    permission_classes = [AllowAny] #取消权限认证
    #search_fields = ['name','description']

    def get_serializer_class(self):
        if self.action == 'QueryMenus':
            return QueryMenusInput
        return SysmenuSerializer
    


    # 覆盖并禁用默认的增删改查方法 如果不需要默认的增删改查 则打开注释
    def create(self, request, *args, **kwargs):
        return Response(status=405)  # 禁用 POST 创建方法
    def list(self, request, *args, **kwargs):
        return Response(status=405)  # 禁用 GET 列表方法
    def retrieve(self, request, *args, **kwargs):
        return Response(status=405)  # 禁用 GET 获取单个资源方法
    def update(self, request, *args, **kwargs):
        return Response(status=405)  # 禁用 PUT 更新方法
    def partial_update(self, request, *args, **kwargs):
        return Response(status=405)  # 禁用 PATCH 更新方法
    def destroy(self, request, *args, **kwargs):
        return Response(status=405)  # 禁用 DELETE 删除方法


    @swagger_auto_schema(query_serializer=QueryMenusInput)
    @action(methods=['get'],detail=False,url_name='QueryMenus')
    def QueryMenus(self,request,*args,**kwargs):

        begintime=datetime.now()
        logger.info("进入方法时间:"+begintime.strftime("%Y-%m-%d %H:%M:%S"))

        serilizer_input=QueryMenusInput(data=request.query_params.dict())
        serilizer_input.is_valid(raise_exception=True)
        Code=serilizer_input.data["Code"]
        Name=serilizer_input.data["Name"]
        TenantId=serilizer_input.data["TenantId"]


        menus_query=Sysmenu.objects.all()
        if Code:
            menus_query=menus_query.filter(code__icontains=Code)
        if Name:
            menus_query=menus_query.filter(name__icontains=Name)
        if TenantId and TenantId>=0:
            menus_query=menus_query.filter(tenantid=TenantId)


        menus_query=menus_query.order_by('-creationtime')

        page = request.query_params.get('page', 1)
        page_size =request.query_params.get('page_size', 10)

        paginator = Paginator(menus_query, page_size)
        total_count = paginator.count 
        # 获取当前页的数据
        try:
            page_objs = paginator.page(page)
        except:
            return JsonResponse({'msg': 'Page not found'}, status=status.HTTP_400_BAD_REQUEST)
        #转换获得的结果
        items=[]
        menus_list=list(page_objs)
        for it in menus_list:
            items.append(SysmenuSerializer(it).data)
        
        datas={'count':total_count,'items':items}
        endtime=datetime.now()
        logger.info("结束方法时间:"+endtime.strftime("%Y-%m-%d %H:%M:%S"))
        
        return JsonResponse(datas, status=status.HTTP_200_OK)

        

