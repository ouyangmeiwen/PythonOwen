from app.dbmodel.liblayer_model import LibLayer
from app.dtos.liblayer_dto import LibLayerDto
from app.utils.stringutils import StringUtils
from app.dtos.liblayer_input import LibLayerInput
from app.utils.objetcmapper import ObjectMapper

class LibLayerMap:
    

    @staticmethod
    def model_to_dto(model: LibLayer) -> LibLayerDto:
        return ObjectMapper.map_fields(model, LibLayerDto(), special_fields={"IsDeleted", "IsEnable"})

        dto = LibLayerDto()
        for field in model.__dict__.keys():
            if hasattr(dto, field):
                value = getattr(model, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable"]:
                    value = StringUtils.to_bool(value)
                setattr(dto, field, value)
        return dto
  
    @staticmethod
    def input_to_model(input: LibLayerInput) -> LibLayer:
        return ObjectMapper.map_fields(input, LibLayer(), special_fields={"IsDeleted", "IsEnable"})

        dt_model = LibLayer()
        for field in input.__dict__.keys():
            if hasattr(dt_model, field):
                value = getattr(input, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable"]:
                    value = 1 if value else 0
                setattr(dt_model, field, value)
        return dt_model

