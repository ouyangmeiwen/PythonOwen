
from rest_framework import serializers
from ..model_list.sysmenu import Sysmenu



class SysmenuSerializer(serializers.ModelSerializer):
    """
    菜单
    """
    class Meta:
        model = Sysmenu
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


        # 处理 isenable 字段，支持字节串和布尔值
        isexternal_value = instance.isexternal
        if isinstance(isexternal_value, bytes):
            # 如果是字节串，将 b'\x01' 转换为 True，b'\x00' 转换为 False
            data['isexternal'] = isexternal_value == b'\x01'
        else:
            data['isexternal'] = bool(isexternal_value)

        # 处理 isenable 字段，支持字节串和布尔值
        isiframe_value = instance.isiframe
        if isinstance(isiframe_value, bytes):
            # 如果是字节串，将 b'\x01' 转换为 True，b'\x00' 转换为 False
            data['isiframe'] = isiframe_value == b'\x01'
        else:
            data['isiframe'] = bool(isiframe_value)
        

        # 处理 isenable 字段，支持字节串和布尔值
        isauthenticate_value = instance.isauthenticate
        if isinstance(isauthenticate_value, bytes):
            # 如果是字节串，将 b'\x01' 转换为 True，b'\x00' 转换为 False
            data['isauthenticate'] = isauthenticate_value == b'\x01'
        else:
            data['isauthenticate'] = bool(isauthenticate_value)

        return data


class QueryMenusInput(serializers.Serializer):
    Code=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    Name=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    TenantId= serializers.IntegerField(required=False,allow_null=True)

