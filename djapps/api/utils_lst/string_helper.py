import uuid
import hashlib
import re
from django.forms.models import model_to_dict
from django.db.models import BooleanField
import base64


def Generate_32bit_uuid():
        # 生成一个随机的UUID
        new_uuid = uuid.uuid4()
        # 使用SHA256哈希函数获取UUID的摘要
        sha256_hash = hashlib.sha256(new_uuid.bytes)
        # 获取哈希的十六进制表示，并截取前32个字符
        uuid_32bit = sha256_hash.hexdigest()[:32]
        return uuid_32bit

"""
将字典中的指定字段从字节串（b'\x00' 或 b'\x01'）转换为布尔值。
:param data: 包含需要转换字段的字典
:param boolean_fields: 需要转换的字段名列表
:return: 转换后的字典
"""
def format_boolean_fields(data,boolean_fields):
    for field in boolean_fields:
        if field in data:
            if(data[field] == b'\x00' or data[field] == False):
                data[field] = False
            else:
                data[field] = True
    return data

# Convert model object to dict and handle 'bytes' fields
def convert_model_to_dict(item):
    # Convert model to dict
    data = model_to_dict(item)
    for field, value in data.items():
        # 判断字段类型，如果是 BooleanField，处理 isdeleted 和 isenable 字段
        if isinstance(item._meta.get_field(field), BooleanField):
            if isinstance(value, bytes):
                data[field] = value == b'\x01'
            else:
                data[field] = bool(value)
        # 对其他字段进行字节串转换为 base64 字符串的处理
        elif isinstance(value, bytes):
            data[field] = base64.b64encode(value).decode('utf-8')
    return data

class StringHelper:

    def __init__(self) -> None:
         pass

    def Truncate_string(self,s, max_length):
        if isinstance(s, str):
            if len(s) > max_length:
                return s[:max_length] + '...'
            return s
        return s
    #格式化字符串只允许数字和字母
    #@staticmethod #非静态类下面的方法要加上self
    def Filter_string(self,input_string):
        # 定义正则表达式，匹配所有非字母和数字的字符
        pattern = re.compile('[^a-zA-Z0-9]')
        # 使用 sub 方法将匹配到的字符替换为空字符串
        filtered_string = pattern.sub('', input_string)
        return filtered_string

    #移除首尾[]
    #@staticmethod #非静态类下面的方法要加上self
    def Strip_string(self,input_string):
        stripped_string = input_string.strip("[]")
        return stripped_string
        
 