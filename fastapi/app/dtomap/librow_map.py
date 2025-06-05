from app.dbmodel.librow_model import LibRow
from app.dtos.librow_dto import LibRowDto
from app.utils.stringutils import StringUtils
from app.dtos.librow_input import LibRowInput

class LibRowMap:
    

    @staticmethod
    def model_to_dto(db_model: LibRow) -> LibRowDto:
        dto = LibRowDto()
        for field in db_model.__dict__.keys():
            if hasattr(dto, field):
                value = getattr(db_model, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable"]:
                    value = StringUtils.to_bool(value)
                setattr(dto, field, value)
        return dto

  
    @staticmethod
    def input_to_model(input: LibRowInput) -> LibRow:
        dt_model = LibRow()
        for field in input.__dict__.keys():
            if hasattr(dt_model, field):
                value = getattr(input, field)
                # 特殊字段转换
                if field in ["IsDeleted", "IsEnable"]:
                    value = 1 if value else 0
                setattr(dt_model, field, value)
        return dt_model
