
from rest_framework import serializers

from  ..model_list.libitem import (Libitem,
                    )


#返回对象
class LibitemSerializer(serializers.ModelSerializer):
    """
    图书对象
    """
    class Meta:
        model = Libitem
        fields = '__all__'
        
    def to_representation(self, instance):
        # 获取序列化后的数据
        data = super().to_representation(instance)

        # 处理 isdeleted 字段，支持字节串和布尔值
        isdeleted_value = instance.isdeleted
        if isinstance(isdeleted_value, bytes):
            # 如果是字节串，将 b'\x01' 转换为 True，b'\x00' 转换为 False
            data['isdeleted'] = isdeleted_value == b'\x01'
        else:
            data['isdeleted'] = bool(isdeleted_value)

        # 处理 isenable 字段，支持字节串和布尔值
        isenable_value = instance.isenable
        if isinstance(isenable_value, bytes):
            # 如果是字节串，将 b'\x01' 转换为 True，b'\x00' 转换为 False
            data['isenable'] = isenable_value == b'\x01'
        else:
            data['isenable'] = bool(isenable_value)

        return data

class LibitemDtoSerializer(serializers.ModelSerializer):
    """
    自定会议图书对象
    """
    msg = serializers.SerializerMethodField()
    class Meta:
        model = Libitem
        fields = ['id','title','callno' ,'author', 'barcode', 'catalogcode','locationname', 'isbn', 'publisher', 'tenantid','creationtime','msg']
    def get_msg(self,obj):
        return obj.remark
    

#输入对象
class ImportExcelSerializer(serializers.Serializer):
    # 自定义输入参数
    Path = serializers.CharField(max_length=100,required=False,allow_null=True,default='d:/2.xlsx')
    Title = serializers.CharField(required=False,allow_null=True,default='题名')
    Author = serializers.CharField(required=False,allow_null=True,default='作者')
    Tid = serializers.CharField(required=False,allow_null=True,default='tid')
    CallNo = serializers.CharField(required=False,allow_null=True,default='索书号')
    ISBN = serializers.CharField(required=False,allow_null=True,default='ISBN')
    CatalogCode = serializers.CharField(required=False,allow_null=True,default='分类号')
    Publisher = serializers.CharField(required=False,allow_null=True,default='出版社')
    PubDate = serializers.CharField(required=False,allow_null=True,default='出版日期')
    Price = serializers.CharField(required=False,allow_null=True,default='单价')
    Pages = serializers.CharField(required=False,allow_null=True,default='页数')
    Barcode = serializers.CharField(required=False,allow_null=True,default='条码号')
    Locationname = serializers.CharField(required=False,allow_null=True,default='当前馆藏地点')
    Tenantid = serializers.IntegerField(required=False,allow_null=True,default='1')


class GetLibItemInputSerializer(serializers.Serializer):
    SkipCount=serializers.IntegerField(required=False,allow_null=True,default='0')
    MaxResultCount=serializers.IntegerField(required=False,allow_null=True,default='100')
    Barcode=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    Title=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    CallNo=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    ISBN=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    TenantId=serializers.IntegerField(required=False,allow_null=True)

    
class BooksInfoInputItemSerializer(serializers.Serializer):
    Tid=serializers.CharField(required=True,allow_null=False)
    Epc=serializers.CharField(required=True,allow_null=False)
    Mac=serializers.CharField(required=False,allow_null=True,allow_blank=True)

#图书信息查询  需要校验TID和EPC条码的匹配性
class BooksInfoSafeInputSerializer(serializers.Serializer):
    Inputs=BooksInfoInputItemSerializer(many=True)


class BooksInfoItemSerializer(serializers.Serializer):
    Tid=serializers.CharField()
    Success=serializers.BooleanField()
    Barcode=serializers.CharField()
    ItemState=serializers.IntegerField()
    Msg=serializers.CharField()
#图书信息查询  需要校验TID和EPC条码的匹配性
class BooksInfoSafeDtoSerializer(serializers.Serializer):
    Items=BooksInfoItemSerializer(many=True)



class BooksInfoByTidInputItemSerializer(serializers.Serializer):
    Tid=serializers.CharField(required=True,allow_null=False)
    Mac=serializers.CharField(required=False,allow_null=True,allow_blank=True)

#图书信息查询  仅仅通过TID查询
class BooksInfoByTidInputSerializer(serializers.Serializer):
    Inputs=BooksInfoByTidInputItemSerializer(many=True)




class BooksInfoByTidSerializer(serializers.Serializer):
    Tid=serializers.CharField()
    Success=serializers.BooleanField()
    Barcode=serializers.CharField()
    ItemState=serializers.IntegerField()
    Msg=serializers.CharField()

#图书信息查询  仅仅通过TID查询
class BooksInfoByTidDtoSerializer(serializers.Serializer):
    Items=BooksInfoByTidSerializer(many=True)


class BooksInfoByEpcInputItemSerializer(serializers.Serializer):
    Epc=serializers.CharField(required=True,allow_null=False)
    Mac=serializers.CharField(required=False,allow_null=True,allow_blank=True)

#图书信息查询  仅仅通过Epc查询
class BooksInfoByEpcInputSeriaizer(serializers.Serializer):
    Inputs=BooksInfoByEpcInputItemSerializer(many=True)


class BooksInfoByEpcSerializer(serializers.Serializer):
    Epc=serializers.CharField()
    Success=serializers.BooleanField()
    Barcode=serializers.CharField()
    ItemState=serializers.IntegerField()
    Msg=serializers.CharField()
class BooksInfoByEpcDtoSerializer(serializers.Serializer):
    Items=BooksInfoByEpcSerializer(many=True)



class GetTagInfosInputItemSerializer(serializers.Serializer):
    Barcode=serializers.CharField(required=True,allow_null=False)
    Tid=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    Epc=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    Mac=serializers.CharField(required=False,allow_null=True,allow_blank=True)

#获取图书标签馆藏信息 定位信息   需要校验图书条码和TID以及EPC的匹配 入参
class GetTagInfosSafeInputSerializer(serializers.Serializer):
    Inputs=GetTagInfosInputItemSerializer(many=True)

class GetTagInfosItemSerializer(serializers.Serializer):
    Success=serializers.BooleanField()
    Barcode=serializers.CharField()
    LocationName=serializers.CharField()
    LocName=serializers.CharField()
    CategoryName=serializers.CharField()
    Msg=serializers.CharField()
#获取图书标签馆藏信息 定位信息   需要校验图书条码和TID以及EPC的匹配 返参
class GetTagInfosSafeDtoSerializer(serializers.Serializer):
    Items=GetTagInfosItemSerializer(many=True)

class GetTagInfosByBarcodeInputItemSerializer(serializers.Serializer):
    Barcode=serializers.CharField(required=True,allow_null=False)
    Mac=serializers.CharField(required=False,allow_null=True,allow_blank=True)
#直接通过条码查询 入参
class GetTagInfosByBarcodeInputSerializer(serializers.Serializer):
    Inputs=GetTagInfosByBarcodeInputItemSerializer(many=True)



class GetTagInfosByBarcodeItemSerializer(serializers.Serializer):
    Success=serializers.BooleanField()
    Barcode=serializers.CharField()
    LocationName=serializers.CharField()
    LocName=serializers.CharField()
    CategoryName=serializers.CharField()
    Msg=serializers.CharField()

#直接通过条码查询 返参
class GetTagInfosByBarcodeDtoSerializer(serializers.Serializer):
    Items=GetTagInfosByBarcodeItemSerializer(many=True)
