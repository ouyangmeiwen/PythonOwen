from app.dbmodel.libitem_model import LibItem
from app.dtos.libitem_dto import LibitemDto
from app.utils.stringutils import StringUtils
from app.dtos.libitem_input import LibitemInput

class LibitemMap:
    # @staticmethod
    # def model_to_dto(db_model: LibItem) -> LibitemDto:
    #     dto = LibitemDto()
    #     for field in db_model.__dict__.keys():
    #         if hasattr(dto, field):
    #             value = getattr(db_model, field)
    #             # 特殊字段转换
    #             if field in ["IsDeleted", "IsEnable"]:
    #                 value = StringUtils.to_bool(value)
    #             setattr(dto, field, value)
    #     return dto

    # @staticmethod
    # def input_to_model(input: LibitemInput) -> LibItem:
    #     dt_model = LibItem()
    #     for field in input.__dict__.keys():
    #         if hasattr(dt_model, field):
    #             value = getattr(input, field)
    #             # 特殊字段转换
    #             if field in ["IsDeleted", "IsEnable"]:
    #                 value = 1 if value else 0
    #             setattr(dt_model, field, value)
    #     return dt_model
    
    
    
    # @staticmethod
    # def model_to_dto(db_model: LibItem) -> LibitemDto:
    #     data = db_model.__dict__.copy()
    #     data["IsDeleted"] = StringUtils.to_bool(data.get("IsDeleted", 0))
    #     data["IsEnable"] = StringUtils.to_bool(data.get("IsEnable", 0))
    #     return LibitemDto(**data)

    # @staticmethod
    # def input_to_model(input: LibitemInput) -> LibItem:
    #     data = input.__dict__.copy()
    #     data["IsDeleted"] = 1 if data.get("IsDeleted", False) else 0
    #     data["IsEnable"] = 1 if data.get("IsEnable", False) else 0
    #     return LibItem(**data)


    @staticmethod
    def model_to_dto(db_model: LibItem) -> LibitemDto:
        """ 直接解包 SQLAlchemy 模型为 Pydantic DTO，并转换特殊字段 """
        data = {k: v for k, v in db_model.__dict__.items() if not k.startswith("_")}  # 过滤 SQLAlchemy 内部字段
        data["IsDeleted"] = StringUtils.to_bool(data.get("IsDeleted", 0))
        data["IsEnable"] = StringUtils.to_bool(data.get("IsEnable", 0))
        return LibitemDto(**data)

    @staticmethod
    def input_to_model(input: LibitemInput) -> LibItem:
        """ 直接解包 Pydantic DTO 为 SQLAlchemy 模型，并转换特殊字段 """
        data = input.model_dump()  # 使用 Pydantic 官方推荐方法
        data["IsDeleted"] = int(data.get("IsDeleted", False))  # 直接转换成 0/1
        data["IsEnable"] = int(data.get("IsEnable", False))  
        return LibItem(**data)
