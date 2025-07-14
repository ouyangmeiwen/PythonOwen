
from django.db import models


class Libitem(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=32)  # Field name made lowercase.
    creationtime = models.DateTimeField(db_column='CreationTime')  # Field name made lowercase.
    creatoruserid = models.BigIntegerField(db_column='CreatorUserId', blank=True, null=True)  # Field name made lowercase.
    lastmodificationtime = models.DateTimeField(db_column='LastModificationTime', blank=True, null=True)  # Field name made lowercase.
    lastmodifieruserid = models.BigIntegerField(db_column='LastModifierUserId', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase. This field type is a guess.
    deleteruserid = models.BigIntegerField(db_column='DeleterUserId', blank=True, null=True)  # Field name made lowercase.
    deletiontime = models.DateTimeField(db_column='DeletionTime', blank=True, null=True)  # Field name made lowercase.
    infoid = models.CharField(db_column='InfoId', max_length=32, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=256)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=256, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=32)  # Field name made lowercase.
    isenable = models.BooleanField(db_column='IsEnable')  # Field name made lowercase. This field type is a guess.
    callno = models.CharField(db_column='CallNo', max_length=64, blank=True, null=True)  # Field name made lowercase.
    precallno = models.CharField(db_column='PreCallNo', max_length=64, blank=True, null=True)  # Field name made lowercase.
    catalogcode = models.CharField(db_column='CatalogCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    itemstate = models.PositiveIntegerField(db_column='ItemState')  # Field name made lowercase.
    pressmarkid = models.CharField(db_column='PressmarkId', max_length=32, blank=True, null=True)  # Field name made lowercase.
    pressmarkname = models.CharField(db_column='PressmarkName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    locationid = models.CharField(db_column='LocationId', max_length=32, blank=True, null=True)  # Field name made lowercase.
    locationname = models.CharField(db_column='LocationName', max_length=128, blank=True, null=True)  # Field name made lowercase.
    bookbarcode = models.CharField(db_column='BookBarcode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', max_length=32, blank=True, null=True)  # Field name made lowercase.
    pubno = models.SmallIntegerField(db_column='PubNo', blank=True, null=True)  # Field name made lowercase.
    publisher = models.CharField(db_column='Publisher', max_length=512, blank=True, null=True)  # Field name made lowercase.
    pubdate = models.CharField(db_column='PubDate', max_length=32, blank=True, null=True)  # Field name made lowercase.
    price = models.CharField(db_column='Price', max_length=32, blank=True, null=True)  # Field name made lowercase.
    pages = models.CharField(db_column='Pages', max_length=32, blank=True, null=True)  # Field name made lowercase.
    summary = models.TextField(db_column='Summary', blank=True, null=True)  # Field name made lowercase.
    itemtype = models.PositiveIntegerField(db_column='ItemType')  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    origintype = models.PositiveIntegerField(db_column='OriginType')  # Field name made lowercase.
    createtype = models.PositiveIntegerField(db_column='CreateType')  # Field name made lowercase.
    tenantid = models.IntegerField(db_column='TenantId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'libitem'
        verbose_name = '终端'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name