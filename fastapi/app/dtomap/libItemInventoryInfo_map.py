

import json
from typing import Type
from app.dbmodel.libItemInventoryInfo_modle import LibItemInventoryInfo
from app.dtos.libItemInventoryInfo_dto import LibItemInventoryInfoDto
from app.dtos.libItemInventoryInfo_Input import LibItemInventoryInfoInput


class LibItemInventoryInfoMap:
    @staticmethod
    def model_to_dto(model:LibItemInventoryInfo)->LibItemInventoryInfoDto:
        """ 将 SQLAlchemy 模型转换为 Pydantic DTO """
        json_data = json.dumps({col.name: getattr(model, col.name) for col in model.__table__.columns}, default=str)
        return LibItemInventoryInfoDto.model_validate_json(json_data)


    @staticmethod
    def input_to_model(input:LibItemInventoryInfoInput)->LibItemInventoryInfo:
        """ 将 Pydantic DTO 转换为 SQLAlchemy 模型 """
        data = json.loads(input.model_dump_json())
        return LibItemInventoryInfo(**data)
