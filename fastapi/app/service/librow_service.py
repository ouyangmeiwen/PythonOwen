
from app.dbmanager.dbutils import Database
from app.dbmodel.librow_model import LibRow
from app.dbmodel.libshelf_model import LibShelf
from app.dbmodel.liblayer_model import LibLayer

from app.dtos.librow_dto import LibRowDto
from app.dtos.librow_input import LibRowInput
from typing import Type, TypeVar, List, Optional, Any, Tuple
from app.utils.stringutils import StringUtils
from app.utils.timeutils import TimeUtils
from app.dbmanager.dbinstance import DB_INSTANCE_ASY
from app.dtomap.librow_map import LibRowMap
from app.dtomap.libshelf_map import LibShelfMap
from app.dtomap.liblayer_map import LibLayerMap
from collections import defaultdict


class LibRowServiceAsync:
    def __init__(self):
        self.DB = DB_INSTANCE_ASY
        # Assuming create_tables can be asynchronous

    async def initialize(self):
        # Assuming create_tables can be asynchronous
        await self.DB.create_tables([LibRow])
    

    async def query_many(self, rowno: Optional[int]) -> List[LibRowDto]:
        filters = []
        if rowno is not None:
            filters.append(LibRow.RowNo == rowno)
        dynamic_kwargs = {"IsDeleted": 0}
        librow_models = await self.DB.where_many(LibRow, *filters, **dynamic_kwargs)

        # 提取 RowIdentity 列表
        row_ids = [model.Id for model in librow_models]
        if not row_ids:
            return []  # 如果为空，直接返回空列表
        

        filters_shelf = []
        dynamic_kwargs_shelf = {"IsDeleted": 0}
        dynamic_kwargs_shelf["IsEnable"] = 1


        # 查询 LibShelf
        filters_shelf = [LibShelf.RowIdentity.in_(row_ids)]
        dynamic_kwargs_shelf = {"IsDeleted": 0, "IsEnable": 1}
        libshelf_models = await self.DB.where_many(LibShelf, *filters_shelf, **dynamic_kwargs_shelf)
        libshelf_models.sort(key=lambda s: s.Code)  # 本地按 ShelfNo 升序排序
        # liblayer_models.sort(key=lambda s: s.ShelfNo, reverse=True)

        # 构建 row_id -> shelves 映射
        # shelves_map = {}
        # for shelf in libshelf_models:
        #     shelves_map.setdefault(shelf.RowIdentity, []).append(shelf)
        
        shelves_map = defaultdict(list)
        for shelf in libshelf_models:
            shelves_map[shelf.RowIdentity].append(shelf)


         # 提取 RowIdentity 列表
        shelf_ids = [model.Id for model in libshelf_models]
        if not shelf_ids:
            return []  # 如果为空，直接返回空列表

        
        # 查询 liblayer
        filters_layer = [LibLayer.ShelfId.in_(shelf_ids)]
        dynamic_kwargs_layer = {"IsDeleted": 0, "IsEnable": 1}
        liblayer_models = await self.DB.where_many(LibLayer, *filters_layer, **dynamic_kwargs_layer)
        liblayer_models.sort(key=lambda s: s.Code) # 本地按 ShelfNo 升序排序
        
        # 构建 shelf_id -> layers 映射
        # layer_map = {}
        # for layer in liblayer_models:
        #     layer_map.setdefault(layer.ShelfId, []).append(layer)
        layer_map = defaultdict(list)
        for layer in liblayer_models:
            layer_map[layer.ShelfId].append(layer)


        # 组装 DTO
        dtos = []
        for row_model in librow_models:
            dto = LibRowMap.model_to_dto(row_model)
            shelf_models = shelves_map.get(row_model.Id, [])
            dto.Shelfs = [LibShelfMap.model_to_dto(s) for s in shelf_models]

            for shelf in dto.Shelfs:
                layer_models = layer_map.get(shelf.Id, [])
                shelf.Layers = [LibLayerMap.model_to_dto(l) for l in layer_models]

            dtos.append(dto)
        return dtos