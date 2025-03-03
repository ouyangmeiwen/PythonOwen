import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import *


from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
import pandas as pd

from datetime import datetime
import os

from django.core.paginator import Paginator
import math


from ..utils_lst import string_helper
from ..model_list.libitem import (Libitem)
from rest_framework.permissions import IsAuthenticated


from ..serializers_list.libitemserializer import (ImportExcelSerializer
                                                ,GetLibItemInputSerializer
                                                ,LibitemDtoSerializer
                                                ,LibitemSerializer
                                                ,BooksInfoSafeInputSerializer
                                                ,BooksInfoSafeDtoSerializer
                                                ,BooksInfoByTidInputSerializer
                                                ,BooksInfoByTidDtoSerializer
                                                ,BooksInfoByEpcInputSeriaizer
                                                ,BooksInfoByEpcSerializer
                                                ,BooksInfoByEpcDtoSerializer
                                                ,GetTagInfosByBarcodeInputSerializer
                                                ,GetTagInfosByBarcodeDtoSerializer
                                                ,GetTagInfosSafeInputSerializer
                                                ,GetTagInfosSafeDtoSerializer       
                                                )
stringhelperinstancet=string_helper.StringHelper()
logger = logging.getLogger('log')
# logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}'.format(response_code, response_headers, response_body[:251]))
# logger.error('请求出错-{}'.format(error))


class LibitemViewSet(ModelViewSet):
    """
    终端操作
    """
    # perms_map = {'get': '*', 'post': 'lcpterminal_create',
    #              'put': 'lcpterminal_update', 'delete': 'lcpterminal_delete'}

    queryset = Libitem.objects.all()
    serializer_class = LibitemSerializer

    # 添加过滤器后端
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # 定义可搜索的字段 用于全文搜索。在多个字段中查找包含特定关键字的记录，通常是进行部分匹配而不是精确匹配。
    #/api/gpi/Libitem/?search=keyword 
    #keyword 在 title or author 字段中忽略大小写 like
    search_fields = ['title','author']

    # 定义可过滤的字段  用于精确过滤字段的值 在以下字段中查找
    #/api/gpi/Libitem/?barcode=123124&callno=123&isbn=123213&tenantid=1
    #filterset_fields = ['barcode', 'callno','isbn','tenantid']


    #/api/gpi/Libitem/?title__icontains=中外哲学&barcode=123124&callno=123&isbn=123213&tenantid=1
    filterset_fields = {
        'barcode': ['exact'],
        'title': ['icontains'],
        'callno': ['exact'],
        'isbn': ['exact'],
        'tenantid': ['exact'],
    }



    # 定义排序字段
    ordering_fields = ['-creationtime', 'barcode']

    #pagination_class = None  #默认开启分页 
    #如果 ordering 设置为 ['pk']，即默认按主键（通常是 id）升序排序。当用户没有在请求中指定排序参数时，数据将按主键的顺序返回。
    ordering = ['pk']

    permission_classes = [AllowAny] #取消权限认证
    # permission_classes=[IsAuthenticated]  #全部接口需要校验 如果单独某一个接口需要校验则将该方法放到方法@action内部
    
    def get_serializer_class(self):
        if self.action == 'ImportExcel':
            return ImportExcelSerializer
        elif self.action == 'GetItemList':
            return GetLibItemInputSerializer
        elif self.action=='BooksInfoSafe':
            return BooksInfoSafeInputSerializer
        elif self.action=='BooksInfoByTid':
            return BooksInfoByTidInputSerializer
        elif self.action=='BooksInfoByEpc':
            return BooksInfoByEpcInputSeriaizer
        elif self.action=='GetTagInfosByBarcode':
            return GetTagInfosByBarcodeInputSerializer
        elif self.action=='GetTagInfosSafe':
            return GetTagInfosSafeInputSerializer

        return LibitemSerializer
    


    # 覆盖并禁用默认的增删改查方法 如果不需要默认的增删改查 则打开注释
    def create(self, request, *args, **kwargs):
        return JsonResponse(status=405)  # 禁用 POST 创建方法
    def list(self, request, *args, **kwargs):
        return JsonResponse(status=405)  # 禁用 GET 列表方法
    def retrieve(self, request, *args, **kwargs):
        return JsonResponse(status=405)  # 禁用 GET 获取单个资源方法
    def update(self, request, *args, **kwargs):
        return JsonResponse(status=405)  # 禁用 PUT 更新方法
    def partial_update(self, request, *args, **kwargs):
        return JsonResponse(status=405)  # 禁用 PATCH 更新方法
    def destroy(self, request, *args, **kwargs):
        return JsonResponse(status=405)  # 禁用 DELETE 删除方法


    @swagger_auto_schema(query_serializer=ImportExcelSerializer)
    @action(methods=['get'], detail=False, url_name='ImportExcel')
    def ImportExcel(self, request, *args, **kwargs):
        begintime=datetime.now()
        logger.info("进入方法时间:"+begintime.strftime("%Y-%m-%d %H:%M:%S"))
        # 使用自定义序列化器验证输入数据
        serializer = ImportExcelSerializer(data=request.query_params.dict()) #接受请求头参数
        serializer.is_valid(raise_exception=True)
        # 从序列化器数据中提取字段
        Path = serializer.data['Path']
        Title = serializer.data['Title']
        Author = serializer.data['Author']
        Tid = serializer.data['Tid']
        CallNo = serializer.data['CallNo']
        ISBN = serializer.data['ISBN']
        CatalogCode = serializer.data['CatalogCode']
        Publisher = serializer.data['Publisher']
        PubDate = serializer.data['PubDate']
        Price = serializer.data['Price']
        Pages = serializer.data['Pages']
        Barcode = serializer.data['Barcode']
        Locationname = serializer.data['Locationname']
        Tenantid=serializer.data['Tenantid']
        if os.path.exists(Path):
            logger.info("文件存在")
        else:
            return JsonResponse({'msg':'文件不存在'}, status=status.HTTP_400_BAD_REQUEST)
        df = pd.read_excel(Path)
        total=len(df)
        logger.info("共产生数据:"+str(total)+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #Libitem.objects.all().delete()
        bulk_item=[]
        index=0
        for row in df.itertuples(index=False, name='Row'):
            dic=dict()
            for column in df.columns:
                try:
                    dic[column]=getattr(row, column)
                except:
                    logger.info(column+'不存在')
            obj=Libitem()
            obj.id=string_helper.Generate_32bit_uuid()
            obj.creationtime=datetime.now()  # 设置开始时间为当前时间
            obj.creatoruserid=None
            obj.lastmodificationtime=None
            obj.lastmodifieruserid=None
            obj.isdeleted=False
            obj.deleteruserid=None
            obj.deletiontime=None
            obj.infoid=None
            if Title in dic:
                obj.title=stringhelperinstancet.Truncate_string(dic[Title],100)
            else:
                obj.title=""
            if Author in dic:
                obj.author=dic[Author]
            else:
                obj.author=""
            if Barcode in dic:
                if math.isnan(dic[Barcode]):
                     obj.barcode=""
                else:
                    obj.barcode=stringhelperinstancet.Strip_string(dic[Barcode])
                    obj.barcode=dic[Barcode]
            else:
                obj.barcode=""
            obj.isenable=True
            if CallNo in dic:
                obj.callno=dic[CallNo]
            else:
                obj.callno=""
            obj.precallno=None
            if CatalogCode in dic:
                obj.catalogcode=dic[CatalogCode]
            else:
                obj.catalogcode=""
            obj.itemstate=3
            obj.pressmarkid=None
            obj.pressmarkname=None
            obj.locationid=None
            if Locationname in dic:
                obj.locationname=dic[Locationname]
            else:
                obj.locationname=""
            obj.bookbarcode=None
            if ISBN in dic:
                obj.isbn=dic[ISBN]
            else:
                obj.isbn=""
            obj.pubno=None
            if Publisher in dic:
                obj.publisher=stringhelperinstancet.Truncate_string(dic[Publisher],100)
            else:
                obj.publisher=""
            if PubDate in dic:
                obj.pubdate=stringhelperinstancet.Truncate_string(dic[PubDate],16)
            else:
                obj.pubdate=""
            if Price in dic:
                obj.price=dic[Price]
            else:
                obj.price=""
            if Pages in dic:
                obj.pages=dic[Pages]
            else:
                obj.pages=""
            obj.summary=None
            obj.itemtype=1
            obj.remark="导入数据"
            obj.origintype=1
            obj.createtype=1
            if isinstance(Tenantid, (int)):
                obj.tenantid=Tenantid
            else:
                obj.tenantid=1
            bulk_item.append(obj)
            index=index+1
            if(len(bulk_item)==1000):
                Libitem.objects.bulk_create(bulk_item)
                bulk_item.clear()
                logger.info('当前插入量:'+str(index*1000))
            if(index==total and len(bulk_item)>0):
                Libitem.objects.bulk_create(bulk_item)
                bulk_item.clear()
                logger.info('最后插入量:'+str(len(bulk_item)))
        
        endtime=datetime.now()
        logger.info("结束方法时间:"+endtime.strftime("%Y-%m-%d %H:%M:%S"))
        logger.info("插入:"+str(total)+",消耗时间:"+str((endtime-begintime).total_seconds())+'秒')
        return JsonResponse([], status=status.HTTP_200_OK)



    @action(methods=['post'],detail=False,url_name='GetItemList') #,permission_classes=[IsAuthenticated]
    def GetItemList(self,request,*args,**kwargs):
        begintime=datetime.now()
        logger.info("进入方法时间:"+begintime.strftime("%Y-%m-%d %H:%M:%S"))
        serializer=GetLibItemInputSerializer(data=request.data) #POST获取数据
        serializer.is_valid(raise_exception=True)
        #获取请求的参数
        SkipCount=serializer.data['SkipCount']
        MaxResultCount=serializer.data['MaxResultCount']

        Barcode=serializer.data['Barcode']
        Title=serializer.data['Title']
        CallNo=serializer.data['CallNo']
        ISBN=serializer.data['ISBN']
        TenantId=serializer.data['TenantId']

        libitemallquery=Libitem.objects.all()
        

        #执行查询
        if Barcode and len(Barcode)>0:
            libitemallquery=libitemallquery.filter(barcode=Barcode)
        if Title and len(Title)>0:
            libitemallquery=libitemallquery.filter(title__icontains=Title)
        if CallNo and len(CallNo)>0:
            libitemallquery=libitemallquery.filter(callno=CallNo)
        if ISBN and len(ISBN)>0:
            libitemallquery=libitemallquery.filter(isbn=ISBN)
        if TenantId and TenantId>0:
            libitemallquery=libitemallquery.filter(tenantid=TenantId)
        #排序处理 在这个例子中，field_name 是你想用来排序的字段名。前缀 - 表示降序排序。如果没有前缀，则表示升序排序。
        libitemallquery=libitemallquery.order_by('-creationtime','barcode')

        # # 获取所有对象
        # queryset = MyModel.objects.all()
        # 获取分页参数
        page_number = SkipCount//MaxResultCount+1
        page_size = MaxResultCount
        # 创建分页器
        paginator = Paginator(libitemallquery, page_size)
        total_count = paginator.count 
        # 获取当前页的数据
        try:
            page_objs = paginator.page(page_number)
        except:
            return JsonResponse({'msg': 'Page not found'}, status=status.HTTP_400_BAD_REQUEST)

        #转换获得的结果
        libitems=list(page_objs)
        #构建返回的结果
        datas=[]

        #循环递归处理
        for item in libitems:
            #转换数据库对象
            data=LibitemSerializer(item).data
            datas.append(data)
        endtime=datetime.now()
        logger.info("结束方法时间:"+endtime.strftime("%Y-%m-%d %H:%M:%S"))
        return JsonResponse({'TotalCount':total_count,'Items':datas}, status=status.HTTP_200_OK)