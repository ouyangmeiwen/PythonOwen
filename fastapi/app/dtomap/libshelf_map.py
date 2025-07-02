from app.dbmodel.dbmodels import Librow as LibRow,Libshelf as LibShelf, Liblayer as LibLayer
from app.dtos.libshelf_dto import LibShelfDto
from app.utils.stringutils import StringUtils
from app.dtos.libshelf_input import LibShelfInput
from app.utils.objetcmapper import ObjectMapper

class LibShelfMap:
    

    @staticmethod
    def model_to_dto(model: LibShelf) -> LibShelfDto:
        return ObjectMapper.map_fields(model, LibShelfDto(), special_fields={"IsDeleted", "IsEnable","IsBosseyed"})
        
        dto = LibShelfDto()
        for field in model.__dict__.keys():
            if hasattr(dto, field):
                value = getattr(model, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable","IsBosseyed"]:
                    value = StringUtils.to_bool(value)
                setattr(dto, field, value)
        return dto

  
    @staticmethod
    def input_to_model(input: LibShelfInput) -> LibShelf:
        return ObjectMapper.map_fields(input, LibShelf(), special_fields={"IsDeleted", "IsEnable","IsBosseyed"})

        dt_model = LibShelf()
        for field in input.__dict__.keys():
            if hasattr(dt_model, field):
                value = getattr(input, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable","IsBosseyed"]:
                    value = 1 if value else 0
                setattr(dt_model, field, value)
        return dt_model
   
