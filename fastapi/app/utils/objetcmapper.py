
from app.utils.stringutils import StringUtils
from pydantic import BaseModel


class ObjectMapper:
    @staticmethod
    def map_fields(source, target, special_fields: set = None):
        special_fields = special_fields or set()

        for field in source.__dict__.keys():
            if hasattr(target, field):
                value = getattr(source, field)
                # 特殊字段处理
                if field in special_fields:
                    if isinstance(target, BaseModel):  # 目标是 DTO
                        value = StringUtils.to_bool(value)
                    else:  # 目标是 SQLAlchemy 模型
                        value = 1 if value else 0
                setattr(target, field, value)
        return target
