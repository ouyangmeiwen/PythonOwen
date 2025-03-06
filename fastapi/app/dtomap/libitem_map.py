
from app.dbmodel.libitem_model import LibItem
from app.dtos.libitem_dto import LibitemDto
from app.utils.stringutils import StringUtils
from app.dtos.libitem_input import LibitemInput

class LibitenmMap:
    @staticmethod
    def model_to_dto(db_model:LibItem)->LibitemDto:
        dto=LibitemDto(Id=db_model.Id)
        dto.CreationTime=db_model.CreationTime
        dto.CreatorUserId=db_model.CreatorUserId
        dto.LastModificationTime=db_model.LastModificationTime
        dto.IsDeleted=StringUtils.to_bool(db_model.IsDeleted)   #db是int，dto 是bool
        dto.DeleterUserId=db_model.DeleterUserId
        dto.DeletionTime=db_model.DeletionTime
        dto.InfoId=db_model.InfoId
        dto.Title=db_model.Title
        dto.Author=db_model.Author
        dto.Barcode=db_model.Barcode
        dto.IsEnable=StringUtils.to_bool(db_model.IsEnable)     #db是int，dto 是bool
        dto.CallNo=db_model.CallNo
        dto.PreCallNo=db_model.PreCallNo
        dto.CatalogCode=db_model.CatalogCode
        dto.ItemState=db_model.ItemState
        dto.PressmarkId=db_model.PressmarkId
        dto.PressmarkName=db_model.PressmarkName
        dto.LocationId=db_model.LocationId
        dto.LocationName=db_model.LocationName
        dto.BookBarcode=db_model.BookBarcode
        dto.ISBN=db_model.ISBN
        dto.PubNo=db_model.PubNo
        dto.Publisher=db_model.Publisher
        dto.PubDate=db_model.PubDate
        dto.Price=db_model.Price
        dto.Pages=db_model.Pages
        dto.Summary=db_model.Summary
        dto.ItemType=db_model.ItemType
        dto.Remark=db_model.Remark
        dto.OriginType=db_model.OriginType
        dto.CreateType=db_model.CreateType
        dto.TenantId=db_model.TenantId
        return dto
    @staticmethod
    def input_to_model(input:LibitemInput)->LibItem:
        dt_model=LibItem(Id=input.Id)
        dt_model.CreationTime=input.CreationTime
        dt_model.CreatorUserId=input.CreatorUserId
        dt_model.LastModificationTime=input.LastModificationTime
        dt_model.IsDeleted=1 if input.IsDeleted else 0
        dt_model.DeleterUserId=input.DeleterUserId
        dt_model.DeletionTime=input.DeletionTime
        dt_model.InfoId=input.InfoId
        dt_model.Title=input.Title
        dt_model.Author=input.Author
        dt_model.Barcode=input.Barcode
        dt_model.IsEnable=1 if input.IsEnable else 0
        dt_model.CallNo=input.CallNo
        dt_model.PreCallNo=input.PreCallNo
        dt_model.CatalogCode=input.CatalogCode
        dt_model.ItemState=input.ItemState
        dt_model.PressmarkId=input.PressmarkId
        dt_model.PressmarkName=input.PressmarkName
        dt_model.LocationId=input.LocationId
        dt_model.LocationName=input.LocationName
        dt_model.BookBarcode=input.BookBarcode
        dt_model.ISBN=input.ISBN
        dt_model.PubNo=input.PubNo
        dt_model.Publisher=input.Publisher
        dt_model.PubDate=input.PubDate
        dt_model.Price=input.Price
        dt_model.Pages=input.Pages
        dt_model.Summary=input.Summary
        dt_model.ItemType=input.ItemType
        dt_model.Remark=input.Remark
        dt_model.OriginType=input.OriginType
        dt_model.CreateType=input.CreateType
        dt_model.TenantId=input.TenantId
        return dt_model