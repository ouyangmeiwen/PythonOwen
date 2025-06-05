from app.dbmodel.libshelf_model import LibShelf
from app.dtos.libshelf_dto import LibShelfDto
from app.utils.stringutils import StringUtils
from app.dtos.libshelf_input import LibShelfInput

class LibShelfMap:
    

    @staticmethod
    def model_to_dto(db_model: LibShelf) -> LibShelfDto:
        
        dto = LibShelfDto()
        for field in db_model.__dict__.keys():
            if hasattr(dto, field):
                value = getattr(db_model, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable","IsBosseyed"]:
                    value = StringUtils.to_bool(value)
                setattr(dto, field, value)
        return dto

  
    @staticmethod
    def input_to_model(input: LibShelfInput) -> LibShelf:
        dt_model = LibShelf()
        for field in input.__dict__.keys():
            if hasattr(dt_model, field):
                value = getattr(input, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable","IsBosseyed"]:
                    value = 1 if value else 0
                setattr(dt_model, field, value)
        return dt_model
   
