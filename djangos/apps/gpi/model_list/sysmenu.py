
from django.db import models
class Sysmenu(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=32)  # Field name made lowercase.
    creationtime = models.DateTimeField(db_column='CreationTime', blank=True, null=True)  # Field name made lowercase.
    creatoruserid = models.BigIntegerField(db_column='CreatorUserId', blank=True, null=True)  # Field name made lowercase.
    lastmodificationtime = models.DateTimeField(db_column='LastModificationTime', blank=True, null=True)  # Field name made lowercase.
    lastmodifieruserid = models.BigIntegerField(db_column='LastModifierUserId', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase. This field type is a guess.
    deleteruserid = models.BigIntegerField(db_column='DeleterUserId', blank=True, null=True)  # Field name made lowercase.
    deletiontime = models.DateTimeField(db_column='DeletionTime', blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=32)  # Field name made lowercase.
    permissionname = models.CharField(db_column='PermissionName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    icon = models.TextField(db_column='Icon', blank=True, null=True)  # Field name made lowercase.
    route = models.CharField(db_column='Route', max_length=128, blank=True, null=True)  # Field name made lowercase.
    parameters = models.CharField(db_column='Parameters', max_length=128, blank=True, null=True)  # Field name made lowercase.
    featuredependency = models.CharField(db_column='FeatureDependency', max_length=64, blank=True, null=True)  # Field name made lowercase.
    isexternal = models.BooleanField(db_column='IsExternal')  # Field name made lowercase. This field type is a guess.
    isiframe = models.BooleanField(db_column='IsIframe')  # Field name made lowercase. This field type is a guess.
    isauthenticate = models.BooleanField(db_column='IsAuthenticate')  # Field name made lowercase. This field type is a guess.
    sortcode = models.IntegerField(db_column='SortCode')  # Field name made lowercase.
    isenable = models.BooleanField(db_column='IsEnable')  # Field name made lowercase. This field type is a guess.
    parentid = models.CharField(db_column='ParentId', max_length=32, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    systemtype = models.PositiveIntegerField(db_column='SystemType')  # Field name made lowercase.
    tenantid = models.IntegerField(db_column='TenantId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sysmenu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
