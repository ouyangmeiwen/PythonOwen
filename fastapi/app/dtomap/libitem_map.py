from app.dbmodel.dbmodels import Libitem as LibItem

from app.dtos.libitem_dto import LibitemDto
from app.utils.stringutils import StringUtils
from app.dtos.libitem_input import LibitemInput
from app.utils.objetcmapper import ObjectMapper

class LibitemMap:
    @staticmethod
    def model_to_dto(model: LibItem) -> LibitemDto:
        return ObjectMapper.map_fields(model, LibitemDto(), special_fields={"IsDeleted", "IsEnable"})
       
        dto = LibitemDto()
        for field in model.__dict__.keys():
            if hasattr(dto, field):
                value = getattr(model, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable"]:
                    value = StringUtils.to_bool(value)
                setattr(dto, field, value)
        return dto

    @staticmethod
    def input_to_model(input: LibitemInput) -> LibItem:
        return ObjectMapper.map_fields(input, LibItem(), special_fields={"IsDeleted", "IsEnable"})
        
        dt_model = LibItem()
        for field in input.__dict__.keys():
            if hasattr(dt_model, field):
                value = getattr(input, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable"]:
                    value = 1 if value else 0
                setattr(dt_model, field, value)
        return dt_model
