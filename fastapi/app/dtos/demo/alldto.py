from pydantic import BaseModel, Field, EmailStr, AnyUrl, IPvAnyAddress, UUID4, conint, confloat, constr
from typing import Optional, List, Dict, Tuple, Set, Union, Literal
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from uuid import UUID
from pathlib import Path

from collections import deque
from typing import Deque

class NestedModel(BaseModel):
    # 嵌套模型示例
    key: str = Field(..., example="sub-key")               # 字符串
    value: int = Field(..., example=100)                   # 整数

    key1: Optional[str] = Field(..., example="sub-key")               # 字符串
    value2: Optional[int] = Field(..., example=100)                   # 整数

class FullTypeDTO(BaseModel):
    # 基本类型
    int_field: int = Field(..., description="整数", example=42)
    float_field: float = Field(..., description="浮点数", example=3.14)
    bool_field: bool = Field(..., description="布尔值", example=True)
    str_field: str = Field(..., description="字符串", example="Hello")

    # 限制类型
    positive_int: conint(gt=0) = Field(..., description="必须大于 0 的整数", example=10)
    bounded_float: confloat(ge=0.0, le=1.0) = Field(..., description="介于 0 到 1 之间的浮点数", example=0.75)
    short_str: constr(min_length=2, max_length=10) = Field(..., description="长度在 2~10 之间的字符串", example="abc")

    # 日期时间
    date_field: date = Field(..., description="日期", example="2025-07-02")
    datetime_field: datetime = Field(..., description="日期时间", example="2025-07-02T15:30:00")
    time_field: time = Field(..., description="时间", example="15:30:00")
    timedelta_field: timedelta = Field(..., description="时间间隔", example="1 day, 2:30:00")

    # 特殊类型
    decimal_field: Decimal = Field(..., description="高精度小数", example="123456.789")
    uuid_field: UUID4 = Field(..., description="UUID v4", example="550e8400-e29b-41d4-a716-446655440000")
    path_field: Path = Field(..., description="文件路径", example="/usr/local/bin")
    url_field: AnyUrl = Field(..., description="任意合法 URL", example="https://example.com")
    email_field: EmailStr = Field(..., description="电子邮件地址", example="user@example.com")
    ip_field: IPvAnyAddress = Field(..., description="IP 地址 (IPv4 或 IPv6)", example="192.168.0.1")

    # 容器类型
    list_field: List[int] = Field(..., description="整数列表", example=[1, 2, 3])
    dict_field: Dict[str, float] = Field(..., description="键为字符串，值为浮点数的字典", example={"a": 1.1, "b": 2.2})
    tuple_field: Tuple[int, str, float] = Field(..., description="固定结构的元组", example=(1, "tuple", 3.0))
    set_field: Set[str] = Field(..., description="字符串集合", example={"apple", "banana"})

    # 可选类型与联合类型
    optional_str: Optional[str] = Field(None, description="可选字符串", example="optional value")
    union_field: Union[str, int] = Field(..., description="可以是字符串或整数", example="123")

    # 枚举型（固定值）
    status: Literal["active", "inactive", "pending"] = Field(..., description="固定枚举值", example="active")

    # 嵌套类型
    sub_item: NestedModel = Field(..., description="嵌套模型")
    sub_items: List[NestedModel] = Field(..., description="嵌套模型列表")

    # 带默认值字段
    default_enabled: bool = Field(default=True, description="默认启用", example=True)

    #适用于上传文件内容、二进制数据（比如图片的 base64）。
    bytes_field: bytes = Field(..., description="二进制数据（bytes）", example="aGVsbG8gd29ybGQ=")
    bytearray_field: bytearray = Field(..., description="可变的字节数组", example="bytearray data")

    #和 Set 一样，但不可变，适用于 hashable 的集合类型。
    frozen_set_field: Set[str] = Field(..., description="不可变字符串集合（frozenset）", example={"a", "b"})
    #队列结构，来自 collections。
    queue_field: Deque[int] = Field(..., description="双端队列", example=[1, 2, 3])

    #表示字段只能为 None，很少见，但合法。
    none_only: None = Field(None, description="只能为 None", example=None)

    #嵌套 Union / Optional 多层嵌套
    complex_union: Union[None, int, str, NestedModel] = Field(
        None, description="支持 int、str、嵌套对象或 None", example="hello"
    )

