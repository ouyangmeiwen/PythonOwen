from typing import Any, List, Optional

from sqlalchemy import BigInteger, Column, DECIMAL, Date, DateTime, Float, ForeignKeyConstraint, Index, Integer, SmallInteger, String, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, BIT, CHAR, DATETIME, DOUBLE, LONGBLOB, LONGTEXT, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Efmigrationshistory(Base):
    __tablename__ = '__efmigrationshistory'

    MigrationId: Mapped[str] = mapped_column(VARCHAR(95), primary_key=True)
    ProductVersion: Mapped[str] = mapped_column(VARCHAR(32))


class Abpauditlogs(Base):
    __tablename__ = 'abpauditlogs'
    __table_args__ = (
        Index('IX_AbpAuditLogs_TenantId_ExecutionDuration', 'TenantId', 'ExecutionDuration'),
        Index('IX_AbpAuditLogs_TenantId_ExecutionTime', 'TenantId', 'ExecutionTime'),
        Index('IX_AbpAuditLogs_TenantId_UserId', 'TenantId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ExecutionTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    ExecutionDuration: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ServiceName: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    MethodName: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    ReturnValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    BrowserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    Exception: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    ImpersonatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ImpersonatorTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    CustomData: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))


class Abpbackgroundjobs(Base):
    __tablename__ = 'abpbackgroundjobs'
    __table_args__ = (
        Index('IX_AbpBackgroundJobs_IsAbandoned_NextTryTime', 'IsAbandoned', 'NextTryTime'),
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    JobType: Mapped[str] = mapped_column(VARCHAR(512))
    JobArgs: Mapped[str] = mapped_column(LONGTEXT)
    TryCount: Mapped[int] = mapped_column(SmallInteger)
    NextTryTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsAbandoned: Mapped[Any] = mapped_column(BIT(1))
    Priority: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastTryTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))


class Abpeditions(Base):
    __tablename__ = 'abpeditions'

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(32))
    DisplayName: Mapped[str] = mapped_column(VARCHAR(64))
    Discriminator: Mapped[str] = mapped_column(LONGTEXT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ExpiringEditionId: Mapped[Optional[int]] = mapped_column(Integer)
    MonthlyPrice: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(65, 30))
    AnnualPrice: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(65, 30))
    TrialDayCount: Mapped[Optional[int]] = mapped_column(Integer)
    WaitingDayAfterExpire: Mapped[Optional[int]] = mapped_column(Integer)

    abpfeatures: Mapped[List['Abpfeatures']] = relationship('Abpfeatures', back_populates='abpeditions')
    abptenants: Mapped[List['Abptenants']] = relationship('Abptenants', back_populates='abpeditions')
    appsubscriptionpayments: Mapped[List['Appsubscriptionpayments']] = relationship('Appsubscriptionpayments', back_populates='abpeditions')


class Abpentitychangesets(Base):
    __tablename__ = 'abpentitychangesets'
    __table_args__ = (
        Index('IX_AbpEntityChangeSets_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_AbpEntityChangeSets_TenantId_Reason', 'TenantId', 'Reason'),
        Index('IX_AbpEntityChangeSets_TenantId_UserId', 'TenantId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    BrowserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ExtensionData: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    ImpersonatorTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ImpersonatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Reason: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)

    abpentitychanges: Mapped[List['Abpentitychanges']] = relationship('Abpentitychanges', back_populates='abpentitychangesets')


class Abplanguages(Base):
    __tablename__ = 'abplanguages'
    __table_args__ = (
        Index('IX_AbpLanguages_TenantId_Name', 'TenantId', 'Name'),
    )

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    DisplayName: Mapped[str] = mapped_column(VARCHAR(64))
    IsDisabled: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    Icon: Mapped[Optional[str]] = mapped_column(VARCHAR(128))


class Abplanguagetexts(Base):
    __tablename__ = 'abplanguagetexts'
    __table_args__ = (
        Index('IX_AbpLanguageTexts_TenantId_Source_LanguageName_Key', 'TenantId', 'Source', 'LanguageName', 'Key'),
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    LanguageName: Mapped[str] = mapped_column(VARCHAR(128))
    Source: Mapped[str] = mapped_column(VARCHAR(128))
    Key: Mapped[str] = mapped_column(VARCHAR(256))
    Value: Mapped[str] = mapped_column(LONGTEXT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Abpnotifications(Base):
    __tablename__ = 'abpnotifications'

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    NotificationName: Mapped[str] = mapped_column(VARCHAR(96))
    Severity: Mapped[int] = mapped_column(TINYINT)
    Discriminator: Mapped[str] = mapped_column(VARCHAR(24), server_default=text("'ext'"))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Data: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    DataTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    EntityTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(250))
    EntityTypeAssemblyQualifiedName: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    EntityId: Mapped[Optional[str]] = mapped_column(VARCHAR(96))
    UserIds: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    ExcludedUserIds: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    TenantIds: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    MessageName: Mapped[Optional[str]] = mapped_column(VARCHAR(96))


class Abpnotificationsubscriptions(Base):
    __tablename__ = 'abpnotificationsubscriptions'
    __table_args__ = (
        Index('IX_AbpNotificationSubscriptions_NotificationName_EntityTypeName~', 'NotificationName', 'EntityTypeName', 'EntityId', 'UserId'),
        Index('IX_AbpNotificationSubscriptions_TenantId_NotificationName_Entit~', 'TenantId', 'NotificationName', 'EntityTypeName', 'EntityId', 'UserId')
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    UserId: Mapped[int] = mapped_column(BigInteger)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    NotificationName: Mapped[Optional[str]] = mapped_column(VARCHAR(96))
    EntityTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(250))
    EntityTypeAssemblyQualifiedName: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    EntityId: Mapped[Optional[str]] = mapped_column(VARCHAR(96))


class Abporganizationunitroles(Base):
    __tablename__ = 'abporganizationunitroles'
    __table_args__ = (
        Index('IX_AbpOrganizationUnitRoles_TenantId_OrganizationUnitId', 'TenantId', 'OrganizationUnitId'),
        Index('IX_AbpOrganizationUnitRoles_TenantId_RoleId', 'TenantId', 'RoleId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    RoleId: Mapped[int] = mapped_column(Integer)
    OrganizationUnitId: Mapped[int] = mapped_column(BigInteger)
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Abporganizationunits(Base):
    __tablename__ = 'abporganizationunits'
    __table_args__ = (
        ForeignKeyConstraint(['ParentId'], ['abporganizationunits.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpOrganizationUnits_AbpOrganizationUnits_ParentId'),
        Index('IX_AbpOrganizationUnits_ParentId', 'ParentId'),
        Index('IX_AbpOrganizationUnits_TenantId_Code', 'TenantId', 'Code')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Code: Mapped[str] = mapped_column(VARCHAR(95))
    DisplayName: Mapped[str] = mapped_column(VARCHAR(128))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ParentId: Mapped[Optional[int]] = mapped_column(BigInteger)

    abporganizationunits: Mapped[Optional['Abporganizationunits']] = relationship('Abporganizationunits', remote_side=[Id], back_populates='abporganizationunits_reverse')
    abporganizationunits_reverse: Mapped[List['Abporganizationunits']] = relationship('Abporganizationunits', remote_side=[ParentId], back_populates='abporganizationunits')


class Abppersistedgrants(Base):
    __tablename__ = 'abppersistedgrants'
    __table_args__ = (
        Index('IX_AbpPersistedGrants_SubjectId_ClientId_Type', 'SubjectId', 'ClientId', 'Type'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(200), primary_key=True)
    Type: Mapped[str] = mapped_column(VARCHAR(50))
    ClientId: Mapped[str] = mapped_column(VARCHAR(200))
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Data: Mapped[str] = mapped_column(LONGTEXT)
    SubjectId: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    Expiration: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))


class Abptenantnotifications(Base):
    __tablename__ = 'abptenantnotifications'
    __table_args__ = (
        Index('IX_AbpTenantNotifications_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    NotificationName: Mapped[str] = mapped_column(VARCHAR(96))
    Severity: Mapped[int] = mapped_column(TINYINT)
    Discriminator: Mapped[str] = mapped_column(VARCHAR(24), server_default=text("'ext'"))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    Data: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    DataTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    EntityTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(250))
    EntityTypeAssemblyQualifiedName: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    EntityId: Mapped[Optional[str]] = mapped_column(VARCHAR(96))
    MessageName: Mapped[Optional[str]] = mapped_column(VARCHAR(96))


class Abpuseraccounts(Base):
    __tablename__ = 'abpuseraccounts'
    __table_args__ = (
        Index('IX_AbpUserAccounts_EmailAddress', 'EmailAddress'),
        Index('IX_AbpUserAccounts_TenantId_EmailAddress', 'TenantId', 'EmailAddress'),
        Index('IX_AbpUserAccounts_TenantId_UserId', 'TenantId', 'UserId'),
        Index('IX_AbpUserAccounts_TenantId_UserName', 'TenantId', 'UserName'),
        Index('IX_AbpUserAccounts_UserName', 'UserName')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    UserId: Mapped[int] = mapped_column(BigInteger)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserLinkId: Mapped[Optional[int]] = mapped_column(BigInteger)
    UserName: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    EmailAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Abpuserloginattempts(Base):
    __tablename__ = 'abpuserloginattempts'
    __table_args__ = (
        Index('IX_AbpUserLoginAttempts_TenancyName_UserNameOrEmailAddress_Resu~', 'TenancyName', 'UserNameOrEmailAddress', 'Result'),
        Index('IX_AbpUserLoginAttempts_UserId_TenantId', 'UserId', 'TenantId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    Result: Mapped[int] = mapped_column(TINYINT)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    TenancyName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    UserNameOrEmailAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    BrowserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(512))


class Abpusernotifications(Base):
    __tablename__ = 'abpusernotifications'
    __table_args__ = (
        Index('IX_AbpUserNotifications_UserId_State_CreationTime', 'UserId', 'State', 'CreationTime'),
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    UserId: Mapped[int] = mapped_column(BigInteger)
    TenantNotificationId: Mapped[str] = mapped_column(CHAR(36))
    State: Mapped[int] = mapped_column(Integer)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Abpusers(Base):
    __tablename__ = 'abpusers'
    __table_args__ = (
        ForeignKeyConstraint(['CreatorUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpUsers_AbpUsers_CreatorUserId'),
        ForeignKeyConstraint(['DeleterUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpUsers_AbpUsers_DeleterUserId'),
        ForeignKeyConstraint(['LastModifierUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpUsers_AbpUsers_LastModifierUserId'),
        Index('IX_AbpUsers_CreatorUserId', 'CreatorUserId'),
        Index('IX_AbpUsers_DeleterUserId', 'DeleterUserId'),
        Index('IX_AbpUsers_LastModifierUserId', 'LastModifierUserId'),
        Index('IX_AbpUsers_TenantId_NormalizedEmailAddress', 'TenantId', 'NormalizedEmailAddress'),
        Index('IX_AbpUsers_TenantId_NormalizedUserName', 'TenantId', 'NormalizedUserName')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    UserName: Mapped[str] = mapped_column(VARCHAR(256))
    EmailAddress: Mapped[str] = mapped_column(VARCHAR(256))
    Name: Mapped[str] = mapped_column(VARCHAR(64))
    Surname: Mapped[str] = mapped_column(VARCHAR(64))
    Password: Mapped[str] = mapped_column(VARCHAR(128))
    AccessFailedCount: Mapped[int] = mapped_column(Integer)
    IsLockoutEnabled: Mapped[Any] = mapped_column(BIT(1))
    IsPhoneNumberConfirmed: Mapped[Any] = mapped_column(BIT(1))
    IsTwoFactorEnabled: Mapped[Any] = mapped_column(BIT(1))
    IsEmailConfirmed: Mapped[Any] = mapped_column(BIT(1))
    IsActive: Mapped[Any] = mapped_column(BIT(1))
    NormalizedUserName: Mapped[str] = mapped_column(VARCHAR(256))
    NormalizedEmailAddress: Mapped[str] = mapped_column(VARCHAR(256))
    ShouldChangePasswordOnNextLogin: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    AuthenticationSource: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    EmailConfirmationCode: Mapped[Optional[str]] = mapped_column(VARCHAR(328))
    PasswordResetCode: Mapped[Optional[str]] = mapped_column(VARCHAR(328))
    LockoutEndDateUtc: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    PhoneNumber: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    SecurityStamp: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ConcurrencyStamp: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ProfilePictureId: Mapped[Optional[str]] = mapped_column(CHAR(36))
    SignInTokenExpireTimeUtc: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    SignInToken: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    GoogleAuthenticatorKey: Mapped[Optional[str]] = mapped_column(LONGTEXT)

    abpusers: Mapped[Optional['Abpusers']] = relationship('Abpusers', remote_side=[Id], foreign_keys=[CreatorUserId], back_populates='abpusers_reverse')
    abpusers_reverse: Mapped[List['Abpusers']] = relationship('Abpusers', remote_side=[CreatorUserId], foreign_keys=[CreatorUserId], back_populates='abpusers')
    abpusers_: Mapped[Optional['Abpusers']] = relationship('Abpusers', remote_side=[Id], foreign_keys=[DeleterUserId], back_populates='abpusers__reverse')
    abpusers__reverse: Mapped[List['Abpusers']] = relationship('Abpusers', remote_side=[DeleterUserId], foreign_keys=[DeleterUserId], back_populates='abpusers_')
    abpusers1: Mapped[Optional['Abpusers']] = relationship('Abpusers', remote_side=[Id], foreign_keys=[LastModifierUserId], back_populates='abpusers1_reverse')
    abpusers1_reverse: Mapped[List['Abpusers']] = relationship('Abpusers', remote_side=[LastModifierUserId], foreign_keys=[LastModifierUserId], back_populates='abpusers1')
    abproles: Mapped[List['Abproles']] = relationship('Abproles', foreign_keys='[Abproles.CreatorUserId]', back_populates='abpusers')
    abproles_: Mapped[List['Abproles']] = relationship('Abproles', foreign_keys='[Abproles.DeleterUserId]', back_populates='abpusers_')
    abproles1: Mapped[List['Abproles']] = relationship('Abproles', foreign_keys='[Abproles.LastModifierUserId]', back_populates='abpusers1')
    abpsettings: Mapped[List['Abpsettings']] = relationship('Abpsettings', back_populates='abpusers')
    abptenants: Mapped[List['Abptenants']] = relationship('Abptenants', foreign_keys='[Abptenants.CreatorUserId]', back_populates='abpusers')
    abptenants_: Mapped[List['Abptenants']] = relationship('Abptenants', foreign_keys='[Abptenants.DeleterUserId]', back_populates='abpusers_')
    abptenants1: Mapped[List['Abptenants']] = relationship('Abptenants', foreign_keys='[Abptenants.LastModifierUserId]', back_populates='abpusers1')
    abpuserclaims: Mapped[List['Abpuserclaims']] = relationship('Abpuserclaims', back_populates='abpusers')
    abpuserlogins: Mapped[List['Abpuserlogins']] = relationship('Abpuserlogins', back_populates='abpusers')
    abpuserorganizationunits: Mapped[List['Abpuserorganizationunits']] = relationship('Abpuserorganizationunits', back_populates='abpusers')
    abpuserroles: Mapped[List['Abpuserroles']] = relationship('Abpuserroles', back_populates='abpusers')
    abpusertokens: Mapped[List['Abpusertokens']] = relationship('Abpusertokens', back_populates='abpusers')
    abppermissions: Mapped[List['Abppermissions']] = relationship('Abppermissions', back_populates='abpusers')


class Appaliuser(Base):
    __tablename__ = 'appaliuser'
    __table_args__ = (
        Index('IX_AppAliUser_TenantId_AliUserId', 'TenantId', 'AliUserId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    AliUserId: Mapped[str] = mapped_column(VARCHAR(16))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Avatar: Mapped[Optional[str]] = mapped_column(VARCHAR(400))
    Province: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    City: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    NickName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    IsStudentCertified: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    UserType: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    UserStatus: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    IsCertified: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    Gender: Mapped[Optional[str]] = mapped_column(VARCHAR(10))


class Appapprovalinfo(Base):
    __tablename__ = 'appapprovalinfo'
    __table_args__ = (
        Index('IX_AppApprovalInfo_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_AppApprovalInfo_TenantId_SpTemplateId', 'TenantId', 'SpTemplateId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    SpNo: Mapped[str] = mapped_column(VARCHAR(32))
    SpCreatorUserId: Mapped[str] = mapped_column(VARCHAR(32))
    SpCreatorUserName: Mapped[str] = mapped_column(VARCHAR(32))
    SpTemplateId: Mapped[str] = mapped_column(VARCHAR(64))
    SpStatus: Mapped[int] = mapped_column(TINYINT)
    UseTemplateApprover: Mapped[Any] = mapped_column(BIT(1))
    ChooseDepartment: Mapped[int] = mapped_column(BigInteger)
    Approver: Mapped[str] = mapped_column(VARCHAR(512))
    NotifyType: Mapped[int] = mapped_column(TINYINT)
    ApplyData: Mapped[str] = mapped_column(LONGTEXT)
    SummaryList: Mapped[str] = mapped_column(VARCHAR(2000))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Notifyer: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Appapprovaltemplate(Base):
    __tablename__ = 'appapprovaltemplate'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    SpTemplateId: Mapped[str] = mapped_column(VARCHAR(64))
    SpTemplateName: Mapped[str] = mapped_column(VARCHAR(32))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Appbinaryobjects(Base):
    __tablename__ = 'appbinaryobjects'
    __table_args__ = (
        Index('IX_AppBinaryObjects_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    Bytes: Mapped[bytes] = mapped_column(LONGBLOB)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Appbookorder(Base):
    __tablename__ = 'appbookorder'
    __table_args__ = (
        Index('IX_AppBookOrder_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_AppBookOrder_TenantId_PatronId_PatronBarcode', 'TenantId', 'PatronId', 'PatronBarcode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    BookOrderStatus: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    SubBookInfoId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    SubBookInfoISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    SubBookInfoTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Appchatmessages(Base):
    __tablename__ = 'appchatmessages'
    __table_args__ = (
        Index('IX_AppChatMessages_TargetTenantId_TargetUserId_ReadState', 'TargetTenantId', 'TargetUserId', 'ReadState'),
        Index('IX_AppChatMessages_TargetTenantId_UserId_ReadState', 'TargetTenantId', 'UserId', 'ReadState'),
        Index('IX_AppChatMessages_TenantId_TargetUserId_ReadState', 'TenantId', 'TargetUserId', 'ReadState'),
        Index('IX_AppChatMessages_TenantId_UserId_ReadState', 'TenantId', 'UserId', 'ReadState')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    UserId: Mapped[int] = mapped_column(BigInteger)
    TargetUserId: Mapped[int] = mapped_column(BigInteger)
    Message: Mapped[str] = mapped_column(LONGTEXT)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Side: Mapped[int] = mapped_column(Integer)
    ReadState: Mapped[int] = mapped_column(Integer)
    ReceiverReadState: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    TargetTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    SharedMessageId: Mapped[Optional[str]] = mapped_column(CHAR(36))


class Appcreditloginorder(Base):
    __tablename__ = 'appcreditloginorder'
    __table_args__ = (
        Index('IX_AppCreditLoginOrder_TenantId_AliUserId', 'TenantId', 'AliUserId'),
        Index('IX_AppCreditLoginOrder_TenantId_CreationTime', 'TenantId', 'CreationTime')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    OutTransNo: Mapped[str] = mapped_column(VARCHAR(64))
    IsAdmit: Mapped[Any] = mapped_column(BIT(1))
    IsSuccess: Mapped[Any] = mapped_column(BIT(1))
    IsCancel: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    QrUrl: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    Code: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Message: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CertType: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CertName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CertNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    AliUserId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Appfriendships(Base):
    __tablename__ = 'appfriendships'
    __table_args__ = (
        Index('IX_AppFriendships_FriendTenantId_FriendUserId', 'FriendTenantId', 'FriendUserId'),
        Index('IX_AppFriendships_FriendTenantId_UserId', 'FriendTenantId', 'UserId'),
        Index('IX_AppFriendships_TenantId_FriendUserId', 'TenantId', 'FriendUserId'),
        Index('IX_AppFriendships_TenantId_UserId', 'TenantId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    UserId: Mapped[int] = mapped_column(BigInteger)
    FriendUserId: Mapped[int] = mapped_column(BigInteger)
    FriendUserName: Mapped[str] = mapped_column(VARCHAR(256))
    State: Mapped[int] = mapped_column(Integer)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    FriendTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    FriendTenancyName: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    FriendProfilePictureId: Mapped[Optional[str]] = mapped_column(CHAR(36))


class Appinvoices(Base):
    __tablename__ = 'appinvoices'

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    InvoiceDate: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    InvoiceNo: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    TenantLegalName: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    TenantAddress: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    TenantTaxNo: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Appitemlocked(Base):
    __tablename__ = 'appitemlocked'
    __table_args__ = (
        Index('IX_AppItemLocked_TenantId_ItemId_ItemBarcode', 'TenantId', 'ItemId', 'ItemBarcode'),
        Index('IX_AppItemLocked_TenantId_PatronId_PatronBarcode', 'TenantId', 'PatronId', 'PatronBarcode'),
        Index('IX_AppItemLocked_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    PatronId: Mapped[str] = mapped_column(VARCHAR(32))
    SerialNo: Mapped[str] = mapped_column(VARCHAR(32))
    PatronName: Mapped[str] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[str] = mapped_column(VARCHAR(64))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    TerminalShelfId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalShelfName: Mapped[str] = mapped_column(VARCHAR(128))
    ItemId: Mapped[str] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[str] = mapped_column(VARCHAR(256))
    ItemBarcode: Mapped[str] = mapped_column(VARCHAR(32))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    IsCanceled: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemAuthor: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LockStartTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LockEndTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    PickUpTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))


class Appmessageboard(Base):
    __tablename__ = 'appmessageboard'
    __table_args__ = (
        Index('IX_AppMessageBoard_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_AppMessageBoard_TenantId_OpenId_PatronId_PatronBarcode', 'TenantId', 'OpenId', 'PatronId', 'PatronBarcode'),
        Index('IX_AppMessageBoard_TenantId_ParentId', 'TenantId', 'ParentId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Content: Mapped[str] = mapped_column(VARCHAR(2000))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    OpenId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ParentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    AttachmentId: Mapped[Optional[str]] = mapped_column(VARCHAR(512))


class Appnotificationlog(Base):
    __tablename__ = 'appnotificationlog'
    __table_args__ = (
        Index('IX_AppNotificationLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_AppNotificationLog_TenantId_SendTo', 'TenantId', 'SendTo')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TemplateSourceType: Mapped[int] = mapped_column(TINYINT)
    NotificationType: Mapped[int] = mapped_column(TINYINT)
    TemplateMessageType: Mapped[int] = mapped_column(TINYINT)
    SendTo: Mapped[str] = mapped_column(VARCHAR(64))
    Result: Mapped[int] = mapped_column(TINYINT)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    IsRead: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TemplateId: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Title: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    MessageContent: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    MessageId: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Code: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Apppayorder(Base):
    __tablename__ = 'apppayorder'
    __table_args__ = (
        Index('IX_AppPayOrder_TenantId_CreationTime', 'TenantId', 'CreationTime'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    OutTradeNo: Mapped[str] = mapped_column(VARCHAR(32))
    AppId: Mapped[str] = mapped_column(VARCHAR(32))
    PaymentStatus: Mapped[int] = mapped_column(TINYINT)
    PayMoney: Mapped[int] = mapped_column(Integer)
    PaymentType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    AppOrderNo: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    DeviceInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    BodyInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    DetailInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    QrCodeUrl: Mapped[Optional[str]] = mapped_column(VARCHAR(128))


class Apppickupcode(Base):
    __tablename__ = 'apppickupcode'
    __table_args__ = (
        Index('IX_AppPickupCode_TenantId_CreationTime', 'TenantId', 'CreationTime'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Code: Mapped[str] = mapped_column(CHAR(8))
    SerialNo: Mapped[str] = mapped_column(VARCHAR(32))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    OverdueTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))


class Appqrcode(Base):
    __tablename__ = 'appqrcode'
    __table_args__ = (
        Index('IX_AppQrCode_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_AppQrCode_TenantId_OpenId', 'TenantId', 'OpenId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    OpenId: Mapped[str] = mapped_column(VARCHAR(32))
    ExpireSeconds: Mapped[int] = mapped_column(Integer)
    QrUrl: Mapped[str] = mapped_column(VARCHAR(256))
    ExpireTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Ticket: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Apprecommendinfo(Base):
    __tablename__ = 'apprecommendinfo'
    __table_args__ = (
        Index('IX_AppRecommendInfo_TenantId_CreationTime', 'TenantId', 'CreationTime'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    Title: Mapped[str] = mapped_column(VARCHAR(256))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Author: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Publisher: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Appsubbookinfo(Base):
    __tablename__ = 'appsubbookinfo'
    __table_args__ = (
        Index('IX_AppSubBookInfo_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_AppSubBookInfo_TenantId_ISBN', 'TenantId', 'ISBN'),
        Index('IX_AppSubBookInfo_TenantId_IsDeleted', 'TenantId', 'IsDeleted')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    ISBN: Mapped[str] = mapped_column(VARCHAR(32))
    Title: Mapped[str] = mapped_column(VARCHAR(256))
    IsRecommend: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Author: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    AuthorCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Publisher: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PubDate: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CatalogCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Language: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Price: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Pages: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Format: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Image: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Summary: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Tags: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Series: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Barcodes: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Appusercard(Base):
    __tablename__ = 'appusercard'
    __table_args__ = (
        Index('IX_AppUserCard_TenantId_IsDeleted', 'TenantId', 'IsDeleted'),
        Index('IX_AppUserCard_TenantId_OpenId_CardNo', 'TenantId', 'OpenId', 'CardNo')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    OpenId: Mapped[str] = mapped_column(VARCHAR(255))
    CardNo: Mapped[str] = mapped_column(VARCHAR(255))
    AppType: Mapped[int] = mapped_column(TINYINT)
    RoleType: Mapped[int] = mapped_column(TINYINT)
    IsEnabled: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Password: Mapped[Optional[str]] = mapped_column(VARCHAR(512))


class Appweuser(Base):
    __tablename__ = 'appweuser'
    __table_args__ = (
        Index('IX_AppWeUser_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_AppWeUser_TenantId_OpenId', 'TenantId', 'OpenId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    OpenId: Mapped[str] = mapped_column(VARCHAR(32))
    Sex: Mapped[int] = mapped_column(TINYINT)
    Subscribe: Mapped[int] = mapped_column(SmallInteger)
    WeUserType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    NickName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Language: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    City: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Province: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Country: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    HeadImgUrl: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    SubscribeTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    UnionId: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


t_bookcaseinfo = Table(
    'bookcaseinfo', Base.metadata,
    Column('nBookCaseInfoID', VARCHAR(255)),
    Column('nEPCOrder', BigInteger),
    Column('szBookCaseCode', VARCHAR(50)),
    Column('nBookCaseLayers', Integer),
    Column('nBuildingNo', Integer),
    Column('nFloorNo', Integer),
    Column('nRoomNo', Integer),
    Column('szMemo', VARCHAR(255)),
    Column('nX1', DOUBLE),
    Column('nY1', DOUBLE),
    Column('nX2', DOUBLE),
    Column('nY2', DOUBLE),
    Column('nBookCount', Integer),
    Column('nID', Integer),
    Column('nAngel', DOUBLE),
    Column('szCaseNoTrans', VARCHAR(50)),
    Column('bBosseyed', TINYINT),
    Column('bNewShelves', TINYINT)
)


class Dasbusinesscount(Base):
    __tablename__ = 'dasbusinesscount'

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Type: Mapped[str] = mapped_column(VARCHAR(32))
    Time: Mapped[str] = mapped_column(VARCHAR(32))
    Count: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Business: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Dascirculatecount(Base):
    __tablename__ = 'dascirculatecount'
    __table_args__ = (
        Index('IX_DasCirculateCount_TenantId_StartTime', 'TenantId', 'StartTime'),
        Index('IX_DasCirculateCount_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    StartTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    EndTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Type: Mapped[int] = mapped_column(TINYINT)
    Result: Mapped[int] = mapped_column(TINYINT)
    Count: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))


class Dasdatabaselink(Base):
    __tablename__ = 'dasdatabaselink'

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ConnectionString: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Dasdatasource(Base):
    __tablename__ = 'dasdatasource'

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    DbLinkId: Mapped[str] = mapped_column(CHAR(36))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Code: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Sql: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Dasfeecount(Base):
    __tablename__ = 'dasfeecount'
    __table_args__ = (
        Index('IX_DasFeeCount_TenantId_StartTime', 'TenantId', 'StartTime'),
        Index('IX_DasFeeCount_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    StartTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    EndTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    FeeType: Mapped[int] = mapped_column(TINYINT)
    PaymentType: Mapped[int] = mapped_column(TINYINT)
    Amount: Mapped[int] = mapped_column(Integer)
    Count: Mapped[int] = mapped_column(Integer)
    Result: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))


class Daspatronlogcount(Base):
    __tablename__ = 'daspatronlogcount'
    __table_args__ = (
        Index('IX_DasPatronLogCount_TenantId_StartTime', 'TenantId', 'StartTime'),
        Index('IX_DasPatronLogCount_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    StartTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    EndTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    PatronLogType: Mapped[int] = mapped_column(TINYINT)
    PatronLogMode: Mapped[int] = mapped_column(SmallInteger)
    Result: Mapped[int] = mapped_column(TINYINT)
    Count: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CardTypeId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CardTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))


class Dasperformance(Base):
    __tablename__ = 'dasperformance'
    __table_args__ = (
        Index('IX_DasPerformance_CreationTime', 'CreationTime'),
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Current_CPU_Usage: Mapped[float] = mapped_column(Float)
    Available_RAM: Mapped[float] = mapped_column(Float)
    Total_SYS_RAM_In_MB: Mapped[float] = mapped_column(Float)
    Total_SYS_RAM_In_Bytes: Mapped[float] = mapped_column(Float)
    RAM_Used: Mapped[float] = mapped_column(Float)
    Percent_RAM_Used: Mapped[float] = mapped_column(Float)
    System_Performing_Critical: Mapped[Any] = mapped_column(BIT(1))
    CPU_Performing_Critical: Mapped[Any] = mapped_column(BIT(1))
    RAM_Performing_Critical: Mapped[Any] = mapped_column(BIT(1))
    SystemCalls_ByCPU_PerSec: Mapped[float] = mapped_column(Float)
    Get_NumThreads_EachProcessorServing: Mapped[float] = mapped_column(Float)
    NumThreads_CreatedByProcess_Last: Mapped[float] = mapped_column(Float)
    Avg_DiskRead_PerSec: Mapped[float] = mapped_column(Float)
    Avg_DiskWrite_PerSec: Mapped[float] = mapped_column(Float)
    DiskRead_BytesPerSec: Mapped[float] = mapped_column(Float)
    DiskWrite_BytesPerSec: Mapped[float] = mapped_column(Float)
    NetworkReceived_BytesPerSec: Mapped[float] = mapped_column(Float)
    NetworkSent_BytesPerSec: Mapped[float] = mapped_column(Float)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)


class Dassecuritygatecount(Base):
    __tablename__ = 'dassecuritygatecount'
    __table_args__ = (
        Index('IX_DasSecurityGateCount_TenantId_StartTime', 'TenantId', 'StartTime'),
        Index('IX_DasSecurityGateCount_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    StartTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    EndTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TotalInCount: Mapped[int] = mapped_column(Integer)
    TotalOutCount: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))


class Dasvisitpage(Base):
    __tablename__ = 'dasvisitpage'
    __table_args__ = (
        Index('IX_DasVisitPage_TenantId_AppId_ref_date', 'TenantId', 'AppId', 'ref_date'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    page_visit_pv: Mapped[int] = mapped_column(Integer)
    page_staytime_pv: Mapped[decimal.Decimal] = mapped_column(DOUBLE)
    entrypage_pv: Mapped[int] = mapped_column(Integer)
    exitpage_pv: Mapped[int] = mapped_column(Integer)
    page_share_pv: Mapped[int] = mapped_column(Integer)
    page_share_uv: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ref_date: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    page_path: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    page_visit_uv: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    AppId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Dasvisittrend(Base):
    __tablename__ = 'dasvisittrend'
    __table_args__ = (
        Index('IX_DasVisitTrend_TenantId_AppId_ref_date', 'TenantId', 'AppId', 'ref_date'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    session_cnt: Mapped[int] = mapped_column(Integer)
    visit_pv: Mapped[int] = mapped_column(Integer)
    visit_uv: Mapped[int] = mapped_column(Integer)
    visit_uv_new: Mapped[int] = mapped_column(Integer)
    stay_time_uv: Mapped[decimal.Decimal] = mapped_column(DOUBLE)
    stay_time_session: Mapped[decimal.Decimal] = mapped_column(DOUBLE)
    visit_depth: Mapped[decimal.Decimal] = mapped_column(DOUBLE)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ref_date: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    AppId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


t_itemloc010301 = Table(
    'itemloc010301', Base.metadata,
    Column('szBookCaseNo', VARCHAR(50)),
    Column('szBookID', VARCHAR(50)),
    Column('szName', VARCHAR(255)),
    Column('szBookIndex', VARCHAR(50)),
    Column('szlibCD', VARCHAR(100)),
    Column('szAuthor', VARCHAR(100)),
    Column('szPublishName', VARCHAR(200)),
    Column('szISBN', VARCHAR(50)),
    Column('Id', VARCHAR(64))
)


t_items = Table(
    'items', Base.metadata,
    Column('szBookCaseNo', VARCHAR(50)),
    Column('szBookID', VARCHAR(50)),
    Column('szName', VARCHAR(255)),
    Column('szBookIndex', VARCHAR(50)),
    Column('szlibCD', VARCHAR(100)),
    Column('szAuthor', VARCHAR(100)),
    Column('szPublishName', VARCHAR(200)),
    Column('szISBN', VARCHAR(50)),
    Column('itemId', VARCHAR(64)),
    Column('locId', VARCHAR(64))
)


class Lcpcommandlog(Base):
    __tablename__ = 'lcpcommandlog'
    __table_args__ = (
        Index('IX_LcpCommandLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpCommandLog_TenantId_TargetId', 'TenantId', 'TargetId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TargetId: Mapped[str] = mapped_column(VARCHAR(32))
    Command: Mapped[int] = mapped_column(TINYINT)
    CommandLogType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TargetCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TargetName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CommandData: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpconfig(Base):
    __tablename__ = 'lcpconfig'
    __table_args__ = (
        Index('IX_LcpConfig_TenantId_IsDeleted_TargetId', 'TenantId', 'IsDeleted', 'TargetId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TargetId: Mapped[str] = mapped_column(VARCHAR(32))
    FileName: Mapped[str] = mapped_column(VARCHAR(64))
    IsLost: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TargetCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TargetName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Directory: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Content: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpmaintainlog(Base):
    __tablename__ = 'lcpmaintainlog'
    __table_args__ = (
        Index('IX_LcpMaintainLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpMaintainLog_TenantId_TerminalId_TerminalCode', 'TenantId', 'TerminalId', 'TerminalCode'),
        Index('IX_LcpMaintainLog_TenantId_UserId', 'TenantId', 'UserId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    UserId: Mapped[int] = mapped_column(BigInteger)
    Name: Mapped[str] = mapped_column(VARCHAR(64))
    UserName: Mapped[str] = mapped_column(VARCHAR(256))
    MaintainLogType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    MaintainAmount: Mapped[Optional[int]] = mapped_column(Integer)
    MaintainAmountDetail: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    WithDrawAmount: Mapped[Optional[int]] = mapped_column(Integer)
    WithDrawAmountDetail: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CardQuantity: Mapped[Optional[int]] = mapped_column(SmallInteger)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpproduct(Base):
    __tablename__ = 'lcpproduct'
    __table_args__ = (
        Index('IX_LcpProduct_Code', 'Code'),
        Index('IX_LcpProduct_ParentId', 'ParentId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(32))
    IsSupportUpgrade: Mapped[Any] = mapped_column(BIT(1))
    IsSupportOpen: Mapped[Any] = mapped_column(BIT(1))
    Order: Mapped[int] = mapped_column(Integer)
    IsNeedActivate: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ParentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Directory: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Port: Mapped[Optional[int]] = mapped_column(Integer)
    ApplicationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Description: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    TerminalTypes: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    StartupType: Mapped[Optional[int]] = mapped_column(TINYINT)


class Lcprfidantenna(Base):
    __tablename__ = 'lcprfidantenna'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    RfidReaderId: Mapped[str] = mapped_column(VARCHAR(32))
    HubId: Mapped[int] = mapped_column(Integer)
    HubPortId: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcprfidreader(Base):
    __tablename__ = 'lcprfidreader'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    IP: Mapped[str] = mapped_column(VARCHAR(32))
    ConnectionString: Mapped[str] = mapped_column(VARCHAR(32))
    PortType: Mapped[int] = mapped_column(TINYINT)
    MemoryBankType: Mapped[int] = mapped_column(TINYINT)
    Duration: Mapped[int] = mapped_column(Integer)
    Interval: Mapped[int] = mapped_column(Integer)
    LoopCount: Mapped[int] = mapped_column(Integer)
    AntennaInterval: Mapped[int] = mapped_column(Integer)
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpsecuritygatebookaccesslog(Base):
    __tablename__ = 'lcpsecuritygatebookaccesslog'
    __table_args__ = (
        Index('IX_LcpSecurityGateBookAccessLog_AccessTime_TerminalId', 'AccessTime', 'TerminalId'),
        Index('IX_LcpSecurityGateBookAccessLog_ItemBarcode', 'ItemBarcode'),
        Index('IX_LcpSecurityGateBookAccessLog_TerminalName', 'TerminalName')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    AccessTime: Mapped[datetime.datetime] = mapped_column(DateTime)
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    ItemTid: Mapped[str] = mapped_column(VARCHAR(32))
    BookStatus: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    Direction: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpsecuritygatebookdailyaccess(Base):
    __tablename__ = 'lcpsecuritygatebookdailyaccess'
    __table_args__ = (
        Index('IX_LcpSecurityGateBookDailyAccess_AccessDate_TerminalId', 'AccessDate', 'TerminalId', unique=True),
        Index('IX_LcpSecurityGateBookDailyAccess_TerminalName', 'TerminalName')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    AccessDate: Mapped[datetime.date] = mapped_column(Date)
    FirstAccessTime: Mapped[datetime.datetime] = mapped_column(DateTime)
    LastAccessTime: Mapped[datetime.datetime] = mapped_column(DateTime)
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    Incoming: Mapped[int] = mapped_column(Integer)
    Outgoing: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)


class Lcpsecuritygateitemlog(Base):
    __tablename__ = 'lcpsecuritygateitemlog'
    __table_args__ = (
        Index('IX_LcpSecurityGateItemLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpSecurityGateItemLog_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    ItemTid: Mapped[str] = mapped_column(VARCHAR(32))
    Result: Mapped[int] = mapped_column(TINYINT)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    AttachmentIds: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpsecuritygatepatronlog(Base):
    __tablename__ = 'lcpsecuritygatepatronlog'
    __table_args__ = (
        Index('IX_LcpSecurityGatePatronLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpSecurityGatePatronLog_TenantId_StartTime_EndTime', 'TenantId', 'StartTime', 'EndTime'),
        Index('IX_LcpSecurityGatePatronLog_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    StartTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    EndTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TotalInCount: Mapped[int] = mapped_column(Integer)
    TotalOutCount: Mapped[int] = mapped_column(Integer)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)


class Lcpserialport(Base):
    __tablename__ = 'lcpserialport'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    PortName: Mapped[str] = mapped_column(VARCHAR(32))
    BaudRate: Mapped[int] = mapped_column(Integer)
    DataBits: Mapped[int] = mapped_column(TINYINT)
    StopBits: Mapped[int] = mapped_column(TINYINT)
    Parity: Mapped[int] = mapped_column(TINYINT)
    ReadTimeout: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpserialportext(Base):
    __tablename__ = 'lcpserialportext'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    SerialPortId: Mapped[str] = mapped_column(VARCHAR(32))
    HubId: Mapped[int] = mapped_column(Integer)
    SerialPortExtPort: Mapped[int] = mapped_column(Integer)
    LayerId: Mapped[str] = mapped_column(VARCHAR(32))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpservice(Base):
    __tablename__ = 'lcpservice'
    __table_args__ = (
        Index('IX_LcpService_TenantId_IsDeleted', 'TenantId', 'IsDeleted'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    ServiceType: Mapped[int] = mapped_column(TINYINT)
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    IsError: Mapped[Any] = mapped_column(BIT(1))
    VersionCode: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    VersionName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    MAC: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    IP: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ConnStr: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminal(Base):
    __tablename__ = 'lcpterminal'
    __table_args__ = (
        Index('IX_LcpTerminal_TenantId_IsDeleted_Code', 'TenantId', 'IsDeleted', 'Code'),
        Index('IX_LcpTerminal_TenantId_IsDeleted_CreationTime', 'TenantId', 'IsDeleted', 'CreationTime'),
        Index('IX_LcpTerminal_TenantId_TerminalCategory_TerminalType', 'TenantId', 'TerminalCategory', 'TerminalType')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TerminalCategory: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalType: Mapped[str] = mapped_column(VARCHAR(32))
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    VersionCode: Mapped[int] = mapped_column(Integer)
    Longitude: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 6))
    Latitude: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 6))
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    VersionName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Province: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    City: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    District: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Street: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Address: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Mac: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Ip: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    LocationId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Password: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    MachineCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Lcpterminaladvertisement(Base):
    __tablename__ = 'lcpterminaladvertisement'
    __table_args__ = (
        Index('IX_LcpTerminalAdvertisement_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpTerminalAdvertisement_TenantId_TerminalType_TerminalId', 'TenantId', 'TerminalType', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TerminalType: Mapped[str] = mapped_column(VARCHAR(32))
    AttachmentId: Mapped[str] = mapped_column(VARCHAR(32))
    SortCode: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminalbox(Base):
    __tablename__ = 'lcpterminalbox'
    __table_args__ = (
        Index('IX_LcpTerminalBox_TenantId_TerminalId', 'TenantId', 'TerminalId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Name: Mapped[str] = mapped_column(VARCHAR(64))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    IsFull: Mapped[Any] = mapped_column(BIT(1))
    IsDisable: Mapped[Any] = mapped_column(BIT(1))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DisableReason: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminalboxitem(Base):
    __tablename__ = 'lcpterminalboxitem'
    __table_args__ = (
        Index('IX_LcpTerminalBoxItem_TenantId_TerminalId', 'TenantId', 'TerminalId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    BoxName: Mapped[str] = mapped_column(VARCHAR(64))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminaldevice(Base):
    __tablename__ = 'lcpterminaldevice'
    __table_args__ = (
        Index('IX_LcpTerminalDevice_TenantId_IsDeleted_CreationTime', 'TenantId', 'IsDeleted', 'CreationTime'),
        Index('IX_LcpTerminalDevice_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalDeviceType: Mapped[int] = mapped_column(TINYINT)
    Name: Mapped[str] = mapped_column(VARCHAR(64))
    IsError: Mapped[Any] = mapped_column(BIT(1))
    Brand: Mapped[str] = mapped_column(VARCHAR(64))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Model: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Version: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ConnectionString: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminaldevicelog(Base):
    __tablename__ = 'lcpterminaldevicelog'
    __table_args__ = (
        Index('IX_LcpTerminalDeviceLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpTerminalDeviceLog_TenantId_TerminalId_TerminalCode', 'TenantId', 'TerminalId', 'TerminalCode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    TerminalDeviceId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalDeviceType: Mapped[int] = mapped_column(TINYINT)
    IsError: Mapped[Any] = mapped_column(BIT(1))
    Brand: Mapped[str] = mapped_column(VARCHAR(64))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Model: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Version: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminallog(Base):
    __tablename__ = 'lcpterminallog'
    __table_args__ = (
        Index('IX_LcpTerminalLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpTerminalLog_TenantId_TerminalId_TerminalCode', 'TenantId', 'TerminalId', 'TerminalCode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    Business: Mapped[int] = mapped_column(TINYINT)
    TerminalLogType: Mapped[int] = mapped_column(TINYINT)
    ClassName: Mapped[str] = mapped_column(VARCHAR(256))
    MethodName: Mapped[str] = mapped_column(VARCHAR(256))
    Result: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalVersionName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminalpermissions(Base):
    __tablename__ = 'lcpterminalpermissions'
    __table_args__ = (
        Index('IX_LcpTerminalPermissions_TenantId_RoleId', 'TenantId', 'RoleId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    RoleId: Mapped[int] = mapped_column(Integer)
    IsGranted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminalshelf(Base):
    __tablename__ = 'lcpterminalshelf'
    __table_args__ = (
        Index('IX_LcpTerminalShelf_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpTerminalShelf_TenantId_TerminalId', 'TenantId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    ShelfName: Mapped[str] = mapped_column(VARCHAR(64))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    PlcCommand: Mapped[str] = mapped_column(VARCHAR(64))
    IsEmpty: Mapped[Any] = mapped_column(BIT(1))
    IsDisable: Mapped[Any] = mapped_column(BIT(1))
    IsInterference: Mapped[Any] = mapped_column(BIT(1))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    IsReserve: Mapped[Any] = mapped_column(BIT(1))
    ReserveType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemAuthor: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    DisableReason: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ReserveOverdueTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    DisablePatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    DisplayName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))


class Lcpterminalshelfitem(Base):
    __tablename__ = 'lcpterminalshelfitem'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    ShelfId: Mapped[str] = mapped_column(VARCHAR(32))
    ShelfName: Mapped[str] = mapped_column(VARCHAR(64))
    IsReserve: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemShortTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemAuthor: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CatalogCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ReserveType: Mapped[Optional[int]] = mapped_column(TINYINT)
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ReserveDate: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    DisableReason: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpterminalshelflog(Base):
    __tablename__ = 'lcpterminalshelflog'
    __table_args__ = (
        Index('IX_LcpTerminalShelfLog_TenantId', 'TenantId'),
        Index('IX_LcpTerminalShelfLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpTerminalShelfLog_TenantId_OperatorId_OperatorName', 'TenantId', 'OperatorId', 'OperatorName'),
        Index('IX_LcpTerminalShelfLog_TenantId_TerminalId_TerminalCode', 'TenantId', 'TerminalId', 'TerminalCode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TerminalId: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[str] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[str] = mapped_column(VARCHAR(128))
    TerminalShelfName: Mapped[str] = mapped_column(VARCHAR(64))
    TerminalShelfLogType: Mapped[int] = mapped_column(TINYINT)
    IsAdmin: Mapped[Any] = mapped_column(BIT(1))
    Result: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalShelfId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OperatorId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OperatorName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    OperatorAccount: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpupgradelog(Base):
    __tablename__ = 'lcpupgradelog'
    __table_args__ = (
        Index('IX_LcpUpgradeLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpUpgradeLog_TenantId_TargetId_TargetCode', 'TenantId', 'TargetId', 'TargetCode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    OldVersionCode: Mapped[int] = mapped_column(Integer)
    OldVersionName: Mapped[str] = mapped_column(VARCHAR(32))
    UpgradeVersionId: Mapped[str] = mapped_column(VARCHAR(32))
    UpgradeVersionCode: Mapped[int] = mapped_column(Integer)
    UpgradeVersionName: Mapped[str] = mapped_column(VARCHAR(32))
    TargetType: Mapped[str] = mapped_column(VARCHAR(32))
    TargetId: Mapped[str] = mapped_column(VARCHAR(32))
    Result: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TargetCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TargetName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Lcpversion(Base):
    __tablename__ = 'lcpversion'
    __table_args__ = (
        Index('IX_LcpVersion_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LcpVersion_TenantId_VersionType_TargetType', 'TenantId', 'VersionType', 'TargetType')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TargetType: Mapped[str] = mapped_column(VARCHAR(32))
    Code: Mapped[int] = mapped_column(Integer)
    Name: Mapped[str] = mapped_column(VARCHAR(32))
    VersionType: Mapped[int] = mapped_column(TINYINT, server_default=text("'0'"))
    PackageType: Mapped[int] = mapped_column(TINYINT, server_default=text("'1'"))
    StorageMode: Mapped[int] = mapped_column(TINYINT, server_default=text("'1'"))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    AttachmentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Description: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ProductId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Url: Mapped[Optional[str]] = mapped_column(VARCHAR(512))


class Libailibrarainbaseinfo(Base):
    __tablename__ = 'libailibrarainbaseinfo'
    __table_args__ = (
        Index('IX_LibAiLibrarainBaseInfo_TenantId_Zone', 'TenantId', 'Zone'),
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Zone: Mapped[str] = mapped_column(VARCHAR(20))
    ProfileId: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)

    libailibrarainbaseinfoitem: Mapped[List['Libailibrarainbaseinfoitem']] = relationship('Libailibrarainbaseinfoitem', back_populates='libailibrarainbaseinfo')


class Libailibrarainbaseinfoprofile(Base):
    __tablename__ = 'libailibrarainbaseinfoprofile'
    __table_args__ = (
        Index('IX_LibAiLibrarainBaseInfoProfile_TenantId', 'TenantId'),
    )

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Status: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    AppId: Mapped[str] = mapped_column(VARCHAR(60))
    AppKey: Mapped[str] = mapped_column(VARCHAR(200))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastAppliedTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))


class Libailibrarainknowledgefileinfo(Base):
    __tablename__ = 'libailibrarainknowledgefileinfo'
    __table_args__ = (
        Index('IX_LibAiLibrarainKnowledgeFileInfo_TenantId_CreationTime', 'TenantId', 'CreationTime'),
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Category: Mapped[int] = mapped_column(Integer)
    ArchiveName: Mapped[str] = mapped_column(VARCHAR(60))
    FileName: Mapped[str] = mapped_column(VARCHAR(128))
    Status: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    Remark: Mapped[str] = mapped_column(VARCHAR(1024))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastAppliedTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ContentType: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    SyncTicket: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Libailibrarainquestionmetrics(Base):
    __tablename__ = 'libailibrarainquestionmetrics'
    __table_args__ = (
        Index('IX_LibAiLibrarainQuestionMetrics_TenantId_Date', 'TenantId', 'Date'),
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    Date_: Mapped[datetime.date] = mapped_column('Date', Date)
    SessionMetricsId: Mapped[int] = mapped_column(BigInteger)
    Classification: Mapped[int] = mapped_column(Integer)
    Count: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    DeviceId: Mapped[str] = mapped_column(VARCHAR(1024))


class Libailibrarainsessionmetrics(Base):
    __tablename__ = 'libailibrarainsessionmetrics'
    __table_args__ = (
        Index('IX_LibAiLibrarainSessionMetrics_TenantId_Date', 'TenantId', 'Date'),
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    Date_: Mapped[datetime.date] = mapped_column('Date', Date)
    SecondsOfService: Mapped[int] = mapped_column(Integer)
    SecondsOfServiceTotal: Mapped[int] = mapped_column(BigInteger)
    BreakCount: Mapped[int] = mapped_column(Integer)
    SessionCount: Mapped[int] = mapped_column(Integer)
    QuestionsCount: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    DeviceId: Mapped[str] = mapped_column(VARCHAR(1024))


class Libainirobotinfo(Base):
    __tablename__ = 'libainirobotinfo'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Date_: Mapped[Optional[str]] = mapped_column('Date', VARCHAR(32))
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    FlowList: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    InteractionListNum: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    DialogListNum: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    AskListNum: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libbatchinfo(Base):
    __tablename__ = 'libbatchinfo'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    BatchNo: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libbatchoperateindex(Base):
    __tablename__ = 'libbatchoperateindex'
    __table_args__ = (
        Index('IX_LibBatchOperateIndex_TenantId_BatchNo', 'TenantId', 'BatchNo'),
        Index('IX_LibBatchOperateIndex_TenantId_CreationTime', 'TenantId', 'CreationTime')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    BatchOperateType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    FailCount: Mapped[int] = mapped_column(Integer, server_default=text("'0'"))
    SuccessCount: Mapped[int] = mapped_column(Integer, server_default=text("'0'"))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    BatchNo: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))


class Libbatchoperatelog(Base):
    __tablename__ = 'libbatchoperatelog'
    __table_args__ = (
        Index('IX_LibBatchOperateLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibBatchOperateLog_TenantId_IndexId_BatchNo', 'TenantId', 'IndexId', 'BatchNo')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    LayerId: Mapped[str] = mapped_column(VARCHAR(32))
    BatchOperateType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    Result: Mapped[int] = mapped_column(TINYINT, server_default=text("'0'"))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    IndexId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    BatchNo: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Tid: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemState: Mapped[Optional[int]] = mapped_column(TINYINT)
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    LocationId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    LayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Libbookinfo(Base):
    __tablename__ = 'libbookinfo'
    __table_args__ = (
        Index('IX_LibBookInfo_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibBookInfo_TenantId_ISBN', 'TenantId', 'ISBN'),
        Index('IX_LibBookInfo_TenantId_IsDeleted', 'TenantId', 'IsDeleted')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    ISBN: Mapped[str] = mapped_column(VARCHAR(32))
    Title: Mapped[str] = mapped_column(VARCHAR(256))
    IsRecommend: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Author: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    AuthorCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Publisher: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    PubDate: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CatalogCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Language: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Price: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Pages: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Format: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Image: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Summary: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Tags: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Series: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Barcodes: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libcirculatelog(Base):
    __tablename__ = 'libcirculatelog'
    __table_args__ = (
        Index('IX_LibCirculateLog_TenantId_CirculateType_Result', 'TenantId', 'CirculateType', 'Result'),
        Index('IX_LibCirculateLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibCirculateLog_TenantId_ItemBarcode_PatronBarcode', 'TenantId', 'ItemBarcode', 'PatronBarcode'),
        Index('IX_LibCirculateLog_TenantId_TerminalId_TerminalCode', 'TenantId', 'TerminalId', 'TerminalCode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    SerialNo: Mapped[str] = mapped_column(VARCHAR(32))
    ItemType: Mapped[int] = mapped_column(TINYINT)
    CirculateType: Mapped[int] = mapped_column(TINYINT)
    Result: Mapped[int] = mapped_column(TINYINT)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    TerminalShelfId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalShelfName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CardTypeId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CardTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ErrorCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OperateTenantId: Mapped[Optional[int]] = mapped_column(Integer)


class LibcirculatelogBak(Base):
    __tablename__ = 'libcirculatelog_bak'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    SerialNo: Mapped[str] = mapped_column(VARCHAR(32))
    ItemType: Mapped[int] = mapped_column(TINYINT)
    CirculateType: Mapped[int] = mapped_column(TINYINT)
    Result: Mapped[int] = mapped_column(TINYINT)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    TerminalShelfId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalShelfName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CardTypeId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CardTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libfeedback(Base):
    __tablename__ = 'libfeedback'
    __table_args__ = (
        Index('IX_LibFeedback_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibFeedback_TenantId_PatronBarcode', 'TenantId', 'PatronBarcode'),
        Index('IX_LibFeedback_TenantId_TerminalId_TerminalCode', 'TenantId', 'TerminalId', 'TerminalCode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    FeedbackType: Mapped[int] = mapped_column(TINYINT)
    Grade: Mapped[int] = mapped_column(TINYINT)
    MessageCode: Mapped[int] = mapped_column(Integer)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Message: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Contact: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libfeelog(Base):
    __tablename__ = 'libfeelog'
    __table_args__ = (
        Index('IX_LibFeeLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibFeeLog_TenantId_PaymentType_FeeLogType_Result', 'TenantId', 'PaymentType', 'FeeLogType', 'Result'),
        Index('IX_LibFeeLog_TenantId_TerminalId_PatronBarcode', 'TenantId', 'TerminalId', 'PatronBarcode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Amount: Mapped[int] = mapped_column(Integer)
    PaymentType: Mapped[int] = mapped_column(TINYINT)
    FeeLogType: Mapped[int] = mapped_column(TINYINT)
    Result: Mapped[int] = mapped_column(TINYINT)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CardTypeId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CardTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    AmountDetail: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    OperateTenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Libinventorystat(Base):
    __tablename__ = 'libinventorystat'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    StatDate: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    StatType: Mapped[int] = mapped_column(Integer)
    InventoryState: Mapped[int] = mapped_column(Integer)
    InventoryCount: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libinventorytask(Base):
    __tablename__ = 'libinventorytask'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TaskType: Mapped[int] = mapped_column(Integer)
    TriggerSatus: Mapped[int] = mapped_column(Integer)
    Interval: Mapped[int] = mapped_column(Integer)
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TaskName: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    InventoryStartDate: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    InventoryEndDate: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    DeviceType: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    RobotId: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    RobotName: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    RobotRouterId: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    RobotRouterName: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Libinventorywork(Base):
    __tablename__ = 'libinventorywork'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TaskStatus: Mapped[int] = mapped_column(Integer)
    SendStatus: Mapped[int] = mapped_column(Integer)
    TriggerSatus: Mapped[int] = mapped_column(Integer)
    WorkTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TaskId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TaskName: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    WorkStarTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    WorkEndTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    HangFireKey: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Comment: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ExceptionMsg: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    DeviceType: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Libinventoryworkdetail(Base):
    __tablename__ = 'libinventoryworkdetail'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TaskStatus: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    WorkId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ExceptionMsg: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libinventoryworklog(Base):
    __tablename__ = 'libinventoryworklog'
    __table_args__ = (
        Index('IX_LibInventoryWorkLog_TenantId_CreationTime_LayerId', 'TenantId', 'CreationTime', 'LayerId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    OnNum: Mapped[int] = mapped_column(Integer)
    WrongNum: Mapped[int] = mapped_column(Integer)
    BorrowedNum: Mapped[int] = mapped_column(Integer)
    NotOnNum: Mapped[int] = mapped_column(Integer)
    InventoryWorkType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    LayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OriginType: Mapped[Optional[int]] = mapped_column(TINYINT)


class Libitem(Base):
    __tablename__ = 'libitem'
    __table_args__ = (
        Index('IX_LibItem_Book_Search', 'Title', 'Author'),
        Index('IX_LibItem_TenantId_IsDeleted_Barcode', 'TenantId', 'IsDeleted', 'Barcode'),
        Index('IX_LibItem_TenantId_IsDeleted_CreationTime', 'TenantId', 'IsDeleted', 'CreationTime')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Title: Mapped[str] = mapped_column(VARCHAR(256))
    Barcode: Mapped[str] = mapped_column(VARCHAR(32))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    ItemState: Mapped[int] = mapped_column(TINYINT)
    ItemType: Mapped[int] = mapped_column(TINYINT)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    CreateType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    InfoId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Author: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PreCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CatalogCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PressmarkId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PressmarkName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    LocationId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    BookBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PubNo: Mapped[Optional[int]] = mapped_column(SmallInteger)
    Publisher: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    PubDate: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Price: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Pages: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Summary: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libiteminventoryinfo(Base):
    __tablename__ = 'libiteminventoryinfo'
    __table_args__ = (
        Index('IX_LibItemInventoryInfo_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibItemInventoryInfo_TenantId_ItemBarcode', 'TenantId', 'ItemBarcode'),
        Index('IX_LibItemInventoryInfo_TenantId_LayerId', 'TenantId', 'LayerId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    InventoryState: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemTid: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemEpc: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Antenna: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    LayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ExceptionMsg: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    OCRItemAuthor: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    OCRItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    OCRItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OCRItemPublisher: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    OCRItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    OriginType: Mapped[Optional[int]] = mapped_column(TINYINT)
    LayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocLayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocLayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocLayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OffShelfTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))


class Libiteminventorylog(Base):
    __tablename__ = 'libiteminventorylog'
    __table_args__ = (
        Index('IX_LibItemInventoryLog_TenantId_CreationTime_LayerId_ItemBarcode', 'TenantId', 'CreationTime', 'LayerId', 'ItemBarcode'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    ItemBarcode: Mapped[str] = mapped_column(VARCHAR(32))
    InventoryWorkType: Mapped[int] = mapped_column(TINYINT)
    InventoryState: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OffShelfTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    InventoryWorkId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    LayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    LocLayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocLayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocLayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ExceptionMsg: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemAuthor: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemPublisher: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    OriginType: Mapped[Optional[int]] = mapped_column(TINYINT)


class Libitemlocinfo(Base):
    __tablename__ = 'libitemlocinfo'
    __table_args__ = (
        Index('IX_LibItemLocInfo_TenantId_IsDeleted_CreationTime', 'TenantId', 'IsDeleted', 'CreationTime'),
        Index('IX_LibItemLocInfo_TenantId_IsDeleted_ItemBarcode', 'TenantId', 'IsDeleted', 'ItemBarcode'),
        Index('IX_LibItemLocInfo_TenantId_IsDeleted_LayerId_IsPreFlag', 'TenantId', 'IsDeleted', 'LayerId', 'IsPreFlag'),
        Index('IX_LibItemLocInfo_TenantId_IsDeleted_LayerId_ItemBarcode', 'TenantId', 'IsDeleted', 'LayerId', 'ItemBarcode'),
        Index('IX_LibItemLocInfo_TenantId_Iseledted_layercode', 'IsDeleted', 'TenantId', 'LayerCode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    ItemBarcode: Mapped[str] = mapped_column(VARCHAR(32))
    ItemCallNo: Mapped[str] = mapped_column(VARCHAR(64))
    LayerId: Mapped[str] = mapped_column(VARCHAR(32))
    IsPreFlag: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    IsForceSort: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    PreCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    LayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OCRItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    OriginType: Mapped[Optional[int]] = mapped_column(TINYINT)


class Libitemoperateindexlog(Base):
    __tablename__ = 'libitemoperateindexlog'
    __table_args__ = (
        Index('IX_LibItemOperateIndexLog_TenantId_CreationTime_CreatorUserId', 'TenantId', 'CreationTime', 'CreatorUserId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    ItemOperateType: Mapped[int] = mapped_column(TINYINT)
    ItemOperateModeType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libitemoperatelog(Base):
    __tablename__ = 'libitemoperatelog'
    __table_args__ = (
        Index('IX_LibItemOperateLog_TenantId_CreationTime_ItemBarcode', 'TenantId', 'CreationTime', 'ItemBarcode'),
        Index('IX_LibItemOperateLog_TenantId_ItemOperateIndexId_CreatorUserId', 'TenantId', 'ItemOperateIndexId', 'CreatorUserId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    ItemOperateType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    ItemOperateModeType: Mapped[int] = mapped_column(TINYINT, server_default=text("'0'"))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemOperateIndexId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    LocationId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    SrcLayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    SrcLayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    DesLayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    DesLayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    DesLayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    SrcLayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Libjournalinfo(Base):
    __tablename__ = 'libjournalinfo'
    __table_args__ = (
        Index('IX_LibJournalInfo_TenantId_IsDeleted_CreationTime', 'TenantId', 'IsDeleted', 'CreationTime'),
        Index('IX_LibJournalInfo_TenantId_PostCode_CN_ISSN', 'TenantId', 'PostCode', 'CN', 'ISSN')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    PubYear: Mapped[str] = mapped_column(VARCHAR(32))
    Title: Mapped[str] = mapped_column(VARCHAR(256))
    JournalType: Mapped[int] = mapped_column(TINYINT)
    Frequency: Mapped[str] = mapped_column(VARCHAR(32))
    SubscriptionType: Mapped[int] = mapped_column(TINYINT)
    SubscriptionNPer: Mapped[int] = mapped_column(Integer)
    SubscriptionNum: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    PostCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ISSN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Publisher: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Language: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CatalogCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UnitPrice: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    AnnualPrice: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    SubscriptionPrice: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Tags: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Barcodes: Mapped[Optional[str]] = mapped_column(VARCHAR(8000))
    Summary: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Liblabel(Base):
    __tablename__ = 'liblabel'
    __table_args__ = (
        Index('IX_LibLabel_TenantId_Barcode_LabelType', 'TenantId', 'Barcode', 'LabelType'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    TenantId: Mapped[int] = mapped_column(Integer, primary_key=True)
    LabelType: Mapped[int] = mapped_column(TINYINT, server_default=text("'0'"))
    Barcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    EpcOrder: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Liblabeloperatelog(Base):
    __tablename__ = 'liblabeloperatelog'
    __table_args__ = (
        Index('IX_LibLabelOperateLog_TenantId_CreationTime_CreatorUserId', 'TenantId', 'CreationTime', 'CreatorUserId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Tid: Mapped[str] = mapped_column(VARCHAR(32))
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    LabelType: Mapped[int] = mapped_column(TINYINT)
    LabelOperateType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Description: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    OldTid: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))


class Liblayer(Base):
    __tablename__ = 'liblayer'
    __table_args__ = (
        Index('IX_LibLayer_TenantId_IsDeleted_Code_Id', 'TenantId', 'IsDeleted', 'Code', 'Id'),
        Index('IX_LibLayer_TenantId_IsDeleted_ShelfId', 'TenantId', 'IsDeleted', 'ShelfId'),
        Index('IX_LibLayer_TenantId_IsDeleted_Tid', 'TenantId', 'IsDeleted', 'Tid'),
        Index('IX_LibLayer_tenantid_isdeleted_Code', 'IsDeleted', 'Code', 'TenantId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    ShelfId: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    Side: Mapped[str] = mapped_column(VARCHAR(32))
    LayerNo: Mapped[int] = mapped_column(TINYINT)
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Code: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Tid: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PreCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Barcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OriginType: Mapped[Optional[int]] = mapped_column(TINYINT)


class Liblayerindexupdatelog(Base):
    __tablename__ = 'liblayerindexupdatelog'
    __table_args__ = (
        Index('IX_LibLayerIndexUpdateLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    MinLayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    MinLayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    MaxLayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    MaxLayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UpdatedLayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UpdatedLayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UpdateStartTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    UpdateEndTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    MaxLayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    MinLayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UpdatedLayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Libnotificationlog(Base):
    __tablename__ = 'libnotificationlog'
    __table_args__ = (
        Index('IX_LibNotificationLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    SendTo: Mapped[str] = mapped_column(VARCHAR(64))
    NotificationType: Mapped[int] = mapped_column(TINYINT)
    Content: Mapped[str] = mapped_column(VARCHAR(2000))
    Result: Mapped[int] = mapped_column(TINYINT)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libpartonreservation(Base):
    __tablename__ = 'libpartonreservation'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    PatronName: Mapped[str] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[str] = mapped_column(VARCHAR(64))
    ItemBarcode: Mapped[str] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[str] = mapped_column(VARCHAR(256))
    ItemType: Mapped[int] = mapped_column(TINYINT)
    ReserveItemType: Mapped[int] = mapped_column(Integer)
    OverdueTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemAuthor: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemPublisher: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    TernimalID: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Address: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    OnShelfWorker: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OnShelfWorkerTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    OffShelfWorker: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OffShelfWorkerTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    CancelWorker: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CancelWorkerTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    CancelReason: Mapped[Optional[str]] = mapped_column(VARCHAR(512))


class Libpatron(Base):
    __tablename__ = 'libpatron'
    __table_args__ = (
        Index('IX_LibPatron_TenantId_IdCard_Barcode', 'TenantId', 'IdCard', 'Barcode'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(64))
    Barcode: Mapped[str] = mapped_column(VARCHAR(64))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    Sex: Mapped[int] = mapped_column(TINYINT)
    Points: Mapped[int] = mapped_column(Integer)
    DepositMoney: Mapped[int] = mapped_column(Integer)
    Balance: Mapped[int] = mapped_column(Integer)
    LateFee: Mapped[int] = mapped_column(Integer)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    CreateType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    IdCard: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Birthday: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Password: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CardTypeId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CardTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Tid: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Phone: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Email: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Address: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    DepartmentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    DepartmentName: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ExpireTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libpatronitem(Base):
    __tablename__ = 'libpatronitem'
    __table_args__ = (
        Index('IX_LibPatronItem_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibPatronItem_TenantId_PatronId_ItemBarcode', 'TenantId', 'PatronId', 'ItemBarcode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    PatronId: Mapped[str] = mapped_column(VARCHAR(32))
    PatronName: Mapped[str] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[str] = mapped_column(VARCHAR(64))
    ItemId: Mapped[str] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[str] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[str] = mapped_column(VARCHAR(256))
    ItemType: Mapped[int] = mapped_column(TINYINT)
    PatronItemType: Mapped[int] = mapped_column(TINYINT)
    RenewNum: Mapped[int] = mapped_column(Integer)
    OverdueTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemAuthor: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libpatronlog(Base):
    __tablename__ = 'libpatronlog'
    __table_args__ = (
        Index('IX_LibPatronLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibPatronLog_TenantId_PatronLogType_PatronLogMode_Result', 'TenantId', 'PatronLogType', 'PatronLogMode', 'Result'),
        Index('IX_LibPatronLog_TenantId_TerminalId_PatronBarcode', 'TenantId', 'TerminalId', 'PatronBarcode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    PatronLogType: Mapped[int] = mapped_column(TINYINT)
    PatronLogMode: Mapped[int] = mapped_column(SmallInteger)
    Result: Mapped[int] = mapped_column(TINYINT)
    OriginType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TerminalName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CardTypeId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CardTypeName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libpointrobot(Base):
    __tablename__ = 'libpointrobot'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    RobotId: Mapped[str] = mapped_column(VARCHAR(128))
    MapId: Mapped[str] = mapped_column(VARCHAR(512))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    RobotName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    MapName: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libpointsclearing(Base):
    __tablename__ = 'libpointsclearing'
    __table_args__ = (
        Index('IX_LibPointsClearing_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibPointsClearing_TenantId_PatronId_PatronBarcode', 'TenantId', 'PatronId', 'PatronBarcode'),
        Index('IX_LibPointsClearing_TenantId_TaskPackageId', 'TenantId', 'TaskPackageId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    PointsRuleType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TaskPackageId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TaskPackageName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libpointslog(Base):
    __tablename__ = 'libpointslog'
    __table_args__ = (
        Index('IX_LibPointsLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibPointsLog_TenantId_PatronId_PatronBarcode', 'TenantId', 'PatronId', 'PatronBarcode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    PointsRuleType: Mapped[int] = mapped_column(TINYINT)
    Points: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TaskPackageId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    TaskPackageName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Librfidantlayer(Base):
    __tablename__ = 'librfidantlayer'
    __table_args__ = (
        Index('IX_LibRfidAntLayer_TenantId_LayerId_AntennaId', 'TenantId', 'LayerId', 'AntennaId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    AntennaId: Mapped[str] = mapped_column(VARCHAR(32))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LayerId: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Librfidscandetaillog(Base):
    __tablename__ = 'librfidscandetaillog'
    __table_args__ = (
        Index('IX_LibRfidScanDetailLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibRfidScanDetailLog_TenantId_ItemBarcode', 'TenantId', 'ItemBarcode'),
        Index('IX_LibRfidScanDetailLog_TenantId_RfidReaderId', 'TenantId', 'RfidReaderId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    RfidReaderId: Mapped[str] = mapped_column(VARCHAR(32))
    Antenna: Mapped[str] = mapped_column(VARCHAR(256))
    TenantId: Mapped[int] = mapped_column(Integer)
    RecordTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemTid: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemEpc: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Title: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Librfidscanlog(Base):
    __tablename__ = 'librfidscanlog'
    __table_args__ = (
        Index('IX_LibRfidScanLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibRfidScanLog_TenantId_ItemBarcode', 'TenantId', 'ItemBarcode'),
        Index('IX_LibRfidScanLog_TenantId_RfidReaderId', 'TenantId', 'RfidReaderId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    RfidReaderId: Mapped[str] = mapped_column(VARCHAR(32))
    Antenna: Mapped[str] = mapped_column(VARCHAR(256))
    TenantId: Mapped[int] = mapped_column(Integer)
    RecordTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ItemTid: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemEpc: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Title: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Librow(Base):
    __tablename__ = 'librow'
    __table_args__ = (
        Index('IX_LibRow_TenantId_IsDeleted_Code', 'TenantId', 'IsDeleted', 'Code'),
        Index('IX_LibRow_TenantId_IsDeleted_LocationId', 'TenantId', 'IsDeleted', 'LocationId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    RowNo: Mapped[int] = mapped_column(Integer)
    RowType: Mapped[int] = mapped_column(TINYINT)
    RowUsageType: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Code: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CatalogCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Librowcatalog(Base):
    __tablename__ = 'librowcatalog'
    __table_args__ = (
        Index('IX_LibRowCatalog_TenantId_IsDeleted_RowIdentity', 'TenantId', 'IsDeleted', 'RowIdentity'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    RowIdentity: Mapped[str] = mapped_column(VARCHAR(32), server_default=text("''"))
    CatalogDescription: Mapped[str] = mapped_column(VARCHAR(256))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Side: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CatalogCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libscanitemlog(Base):
    __tablename__ = 'libscanitemlog'
    __table_args__ = (
        Index('IX_LibScanItemLog_TenantId_CreationTime_CreatorUserId', 'TenantId', 'CreationTime', 'CreatorUserId'),
        Index('IX_LibScanItemLog_TenantId_ItemBarcode', 'TenantId', 'ItemBarcode'),
        Index('IX_LibScanItemLog_TenantId_SerialNo', 'TenantId', 'SerialNo')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    SerialNo: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    LocationId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))


class Libshelf(Base):
    __tablename__ = 'libshelf'
    __table_args__ = (
        Index('IX_LibShelf_TenantId_IsDeleted_Code', 'TenantId', 'IsDeleted', 'Code'),
        Index('IX_LibShelf_TenantId_IsDeleted_RowIdentity', 'TenantId', 'IsDeleted', 'RowIdentity'),
        Index('IX_LibShelf_TenantId_IsDeleted_StructId', 'TenantId', 'IsDeleted', 'StructId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    ShelfNo: Mapped[int] = mapped_column(Integer)
    RowIdentity: Mapped[str] = mapped_column(VARCHAR(32), server_default=text("''"))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    IsBosseyed: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Code: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Side: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    RfidReaderId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    SerialPortId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    X1: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(7, 2))
    Y1: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(7, 2))
    X2: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(7, 2))
    Y2: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(7, 2))
    Angel: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(7, 2))
    StructId: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    FirstCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    LastCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))


class Libshelfpoint(Base):
    __tablename__ = 'libshelfpoint'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    CreateType: Mapped[int] = mapped_column(Integer)
    OrderNo: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ShelfPointName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ShelfPointShowName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ShelfId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ShelfCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    StructId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    RelationName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    X: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(30, 15))
    Y: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(30, 15))
    Angel: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(30, 15))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    MapId: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    RobotId: Mapped[Optional[str]] = mapped_column(VARCHAR(128))


class Libstruct(Base):
    __tablename__ = 'libstruct'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    BuildNo: Mapped[int] = mapped_column(Integer)
    FloorNo: Mapped[int] = mapped_column(Integer)
    RoomNo: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    BuildingName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    FloorName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    RoomName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Description: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Img: Mapped[Optional[bytes]] = mapped_column(LONGBLOB)
    ExtensionName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libtagtobarcodelog(Base):
    __tablename__ = 'libtagtobarcodelog'
    __table_args__ = (
        Index('IX_LibTagToBarcodeLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibTagToBarcodeLog_TenantId_ItemBarcode', 'TenantId', 'ItemBarcode')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    OperateType: Mapped[int] = mapped_column(Integer)
    IsSuccess: Mapped[Any] = mapped_column(BIT(1))
    IsUpdate: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    IPAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))


class Libtaskitem(Base):
    __tablename__ = 'libtaskitem'
    __table_args__ = (
        Index('IX_LibTaskItem_TenantId_ItemBarcode_TaskPackageId', 'TenantId', 'ItemBarcode', 'TaskPackageId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TaskItemStatus: Mapped[int] = mapped_column(TINYINT)
    ItemId: Mapped[str] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[str] = mapped_column(VARCHAR(32))
    ItemTitle: Mapped[str] = mapped_column(VARCHAR(256))
    CorrectLayerId: Mapped[str] = mapped_column(VARCHAR(32))
    CorrectLayerName: Mapped[str] = mapped_column(VARCHAR(32))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TaskPackageId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemTid: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CorrectLayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Libtaskpackage(Base):
    __tablename__ = 'libtaskpackage'
    __table_args__ = (
        Index('IX_LibTaskPackage_TenantId_TaskPackageStatus_PatronBarcode', 'TenantId', 'TaskPackageStatus', 'PatronBarcode'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(32))
    TaskPackageStatus: Mapped[int] = mapped_column(TINYINT)
    ExpireTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    PatronId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PatronBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PatronName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Libupdatefirstbooklog(Base):
    __tablename__ = 'libupdatefirstbooklog'
    __table_args__ = (
        Index('IX_LibUpdateFirstBookLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
        Index('IX_LibUpdateFirstBookLog_TenantId_LayerId', 'TenantId', 'LayerId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    LayerId: Mapped[str] = mapped_column(VARCHAR(32))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LayerName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PretendCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PreItemId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PreItemBarcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PreItemCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PrePretendCallNo: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    LayerCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PreItemTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Misactivity(Base):
    __tablename__ = 'misactivity'

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Subject: Mapped[str] = mapped_column(VARCHAR(128))
    BeginTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    EndTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Address: Mapped[str] = mapped_column(VARCHAR(128))
    Crowd: Mapped[str] = mapped_column(VARCHAR(128))
    SortCode: Mapped[int] = mapped_column(Integer)
    InformationStatus: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    AttachmentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    MediaType: Mapped[Optional[int]] = mapped_column(TINYINT)


class Mismediainfo(Base):
    __tablename__ = 'mismediainfo'

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(256))
    MediaType: Mapped[int] = mapped_column(TINYINT)
    SortCode: Mapped[int] = mapped_column(Integer)
    InformationStatus: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    AttachmentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Misnews(Base):
    __tablename__ = 'misnews'

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    NewsType: Mapped[int] = mapped_column(TINYINT)
    Title: Mapped[str] = mapped_column(VARCHAR(256))
    Editor: Mapped[str] = mapped_column(VARCHAR(64))
    ReleaseTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    SortCode: Mapped[int] = mapped_column(Integer)
    InformationStatus: Mapped[int] = mapped_column(TINYINT)
    Content: Mapped[str] = mapped_column(LONGTEXT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    CoverId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Tags: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Mistemplate(Base):
    __tablename__ = 'mistemplate'

    Id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Thumbnail: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Config: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    RootId: Mapped[Optional[str]] = mapped_column(CHAR(36))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class OwenAuditlog(Base):
    __tablename__ = 'owen_auditlog'
    __table_args__ = (
        Index('idx_owen_auditlog_created_at', 'created_at'),
        Index('idx_owen_auditlog_deleted_at', 'deleted_at'),
        Index('idx_owen_auditlog_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(BIGINT)
    action: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    request: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_general_ci'))
    response: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_general_ci'))
    error: Mapped[Optional[str]] = mapped_column(String(500, 'utf8mb4_general_ci'))
    status: Mapped[Optional[int]] = mapped_column(BigInteger)
    duration: Mapped[Optional[decimal.Decimal]] = mapped_column(DOUBLE)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=3))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=3))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=3))


class OwenRole(Base):
    __tablename__ = 'owen_role'
    __table_args__ = (
        Index('uni_owen_role_name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    permissions: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_general_ci'))

    owen_user: Mapped[List['OwenUser']] = relationship('OwenUser', back_populates='role')


class OwenScheduledtask(Base):
    __tablename__ = 'owen_scheduledtask'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    task_name: Mapped[str] = mapped_column(String(255, 'utf8mb4_general_ci'))
    schedule_time: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=3))
    next_run_time: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=3))
    status: Mapped[str] = mapped_column(String(50, 'utf8mb4_general_ci'))
    interval_seconds: Mapped[Optional[int]] = mapped_column(BigInteger)
    last_run_time: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=3))


class Rescatalog(Base):
    __tablename__ = 'rescatalog'

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    Level: Mapped[int] = mapped_column(Integer)
    ParentCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Rescipinfo(Base):
    __tablename__ = 'rescipinfo'
    __table_args__ = (
        Index('IX_ResCIPInfo_CIP', 'CIP', unique=True),
        Index('IX_ResCIPInfo_ISBN', 'ISBN'),
        Index('IX_ResCIPInfo_ISBN10', 'ISBN10'),
        Index('IX_ResCIPInfo_ISBN13', 'ISBN13')
    )

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    CIP: Mapped[str] = mapped_column(VARCHAR(32))
    Title: Mapped[str] = mapped_column(VARCHAR(256))
    ISBN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Author: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Series: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Publisher: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PubPlace: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    PubDate: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Edition: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PrintNum: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Price: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Language: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Format: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Binding: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CatalogCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Tags: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Summary: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    CIPData: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Pages: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PrintCount: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ISBN10: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ISBN13: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Resfourcorner(Base):
    __tablename__ = 'resfourcorner'

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Code: Mapped[str] = mapped_column(VARCHAR(16))
    Name: Mapped[str] = mapped_column(VARCHAR(16))


class Resjournalinfo(Base):
    __tablename__ = 'resjournalinfo'
    __table_args__ = (
        Index('IX_ResJournalInfo_CN', 'CN'),
        Index('IX_ResJournalInfo_ISSN', 'ISSN'),
        Index('IX_ResJournalInfo_PostCode', 'PostCode')
    )

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    PubYear: Mapped[str] = mapped_column(VARCHAR(16))
    JournalType: Mapped[int] = mapped_column(TINYINT)
    PostCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    CN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ISSN: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Title: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Frequency: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PubDate: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Publisher: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    SortCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ShortTitle: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Level: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    SubscriptionType: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UnitPrice: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    SubUnitPrice: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    MonthlyPrice: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    AnnualPrice: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    Summary: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Tags: Mapped[Optional[str]] = mapped_column(VARCHAR(64))


class Resnotfound(Base):
    __tablename__ = 'resnotfound'

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ISBN: Mapped[str] = mapped_column(VARCHAR(32))
    IsFind: Mapped[int] = mapped_column(Integer)
    CreateTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Respublisherinfo(Base):
    __tablename__ = 'respublisherinfo'

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    Area: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Address: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ZipCode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Phone: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    PublisherType: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Ssbackgroundjobs(Base):
    __tablename__ = 'ssbackgroundjobs'
    __table_args__ = (
        Index('IX_SsBackgroundJobs_CreationTime', 'CreationTime'),
        Index('IX_SsBackgroundJobs_JobType', 'JobType')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    JobType: Mapped[str] = mapped_column(VARCHAR(512))
    JobArgs: Mapped[str] = mapped_column(LONGTEXT)
    TryCount: Mapped[int] = mapped_column(SmallInteger)
    NextTryTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsAbandoned: Mapped[Any] = mapped_column(BIT(1))
    Priority: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastTryTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))


class Sysattachment(Base):
    __tablename__ = 'sysattachment'
    __table_args__ = (
        Index('IX_SysAttachment_CreationTime', 'CreationTime'),
        Index('IX_SysAttachment_TenantId', 'TenantId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Name: Mapped[str] = mapped_column(VARCHAR(256))
    Length: Mapped[int] = mapped_column(BigInteger)
    Extension: Mapped[str] = mapped_column(VARCHAR(128))
    AttachmentApplyType: Mapped[int] = mapped_column(TINYINT)
    StorageMode: Mapped[int] = mapped_column(TINYINT, server_default=text("'1'"))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Sysauditacslog(Base):
    __tablename__ = 'sysauditacslog'
    __table_args__ = (
        Index('IX_SysAuditACSLog_ExecutionTime', 'ExecutionTime'),
        Index('IX_SysAuditACSLog_TenantId', 'TenantId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ExecutionDuration: Mapped[int] = mapped_column(Integer)
    ExecutionTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    MethodName: Mapped[str] = mapped_column(VARCHAR(256))
    ServiceName: Mapped[str] = mapped_column(VARCHAR(256))
    BrowserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CustomData: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Exception: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    ImpersonatorTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ImpersonatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ReturnValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Sysauditapilog(Base):
    __tablename__ = 'sysauditapilog'
    __table_args__ = (
        Index('IX_SysAuditAPILog_ExecutionTime', 'ExecutionTime'),
        Index('IX_SysAuditAPILog_TenantId', 'TenantId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ExecutionDuration: Mapped[int] = mapped_column(Integer)
    ExecutionTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    MethodName: Mapped[str] = mapped_column(VARCHAR(256))
    ServiceName: Mapped[str] = mapped_column(VARCHAR(256))
    BrowserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CustomData: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Exception: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    ImpersonatorTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ImpersonatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ReturnValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Sysauditapplog(Base):
    __tablename__ = 'sysauditapplog'
    __table_args__ = (
        Index('IX_SysAuditAPPLog_ExecutionTime', 'ExecutionTime'),
        Index('IX_SysAuditAPPLog_TenantId', 'TenantId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ExecutionDuration: Mapped[int] = mapped_column(Integer)
    ExecutionTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    MethodName: Mapped[str] = mapped_column(VARCHAR(256))
    ServiceName: Mapped[str] = mapped_column(VARCHAR(256))
    BrowserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CustomData: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Exception: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    ImpersonatorTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ImpersonatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ReturnValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Sysauditlinklog(Base):
    __tablename__ = 'sysauditlinklog'
    __table_args__ = (
        Index('IX_SysAuditLinkLog_ExecutionTime', 'ExecutionTime'),
        Index('IX_SysAuditLinkLog_TenantId', 'TenantId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ExecutionDuration: Mapped[int] = mapped_column(Integer)
    ExecutionTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    MethodName: Mapped[str] = mapped_column(VARCHAR(256))
    ServiceName: Mapped[str] = mapped_column(VARCHAR(256))
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Exception: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ReturnValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Sysauditlmslog(Base):
    __tablename__ = 'sysauditlmslog'
    __table_args__ = (
        Index('IX_SysAuditLMSLog_ExecutionTime', 'ExecutionTime'),
        Index('IX_SysAuditLMSLog_TenantId', 'TenantId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ExecutionDuration: Mapped[int] = mapped_column(Integer)
    ExecutionTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    MethodName: Mapped[str] = mapped_column(VARCHAR(256))
    ServiceName: Mapped[str] = mapped_column(VARCHAR(256))
    BrowserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CustomData: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Exception: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    ImpersonatorTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ImpersonatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ReturnValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Sysauditsslog(Base):
    __tablename__ = 'sysauditsslog'
    __table_args__ = (
        Index('IX_SysAuditSSLog_ExecutionTime', 'ExecutionTime'),
        Index('IX_SysAuditSSLog_TenantId', 'TenantId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ExecutionDuration: Mapped[int] = mapped_column(Integer)
    ExecutionTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    MethodName: Mapped[str] = mapped_column(VARCHAR(256))
    ServiceName: Mapped[str] = mapped_column(VARCHAR(256))
    BrowserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    ClientIpAddress: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    CustomData: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Exception: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    ImpersonatorTenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ImpersonatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    ReturnValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Sysblocklist(Base):
    __tablename__ = 'sysblocklist'
    __table_args__ = (
        Index('IX_SysBlocklist_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(64))
    Barcode: Mapped[str] = mapped_column(VARCHAR(64))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    IdCard: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    OverdueTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TerminalCategory: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Sysbookblocklist(Base):
    __tablename__ = 'sysbookblocklist'
    __table_args__ = (
        Index('IX_SysBookBlockList_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Barcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Sysbooknumlib(Base):
    __tablename__ = 'sysbooknumlib'
    __table_args__ = (
        Index('IX_SysBookNumLib_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    Year: Mapped[int] = mapped_column(SmallInteger)
    Order: Mapped[int] = mapped_column(Integer)
    IsUsed: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    Barcode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LocationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    BookType: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Sysbooknumset(Base):
    __tablename__ = 'sysbooknumset'
    __table_args__ = (
        Index('IX_SysBookNumSet_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    NumLength: Mapped[int] = mapped_column(SmallInteger)
    IsCRC: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    LocationName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    BookType: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    FontWord: Mapped[Optional[str]] = mapped_column(VARCHAR(10))


class Syscardconfig(Base):
    __tablename__ = 'syscardconfig'
    __table_args__ = (
        Index('IX_SysCardConfig_TenantId_CardTypeId', 'TenantId', 'CardTypeId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    CardTypeId: Mapped[str] = mapped_column(VARCHAR(32))
    ItemType: Mapped[int] = mapped_column(TINYINT)
    CheckoutDays: Mapped[int] = mapped_column(SmallInteger)
    MaxCheckout: Mapped[int] = mapped_column(SmallInteger)
    MaxOverdue: Mapped[int] = mapped_column(SmallInteger)
    LateFee: Mapped[int] = mapped_column(SmallInteger)
    RenewNum: Mapped[int] = mapped_column(SmallInteger)
    CanRenewTime: Mapped[int] = mapped_column(SmallInteger)
    RenewDays: Mapped[int] = mapped_column(SmallInteger)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)


class Syscarddevdtl(Base):
    __tablename__ = 'syscarddevdtl'
    __table_args__ = (
        Index('IX_SysCardDevDtl_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    bValid: Mapped[Any] = mapped_column(BIT(1))
    bDEV_01: Mapped[Any] = mapped_column(BIT(1))
    bDEV_02: Mapped[Any] = mapped_column(BIT(1))
    bDEV_03: Mapped[Any] = mapped_column(BIT(1))
    bDEV_04: Mapped[Any] = mapped_column(BIT(1))
    bDEV_05: Mapped[Any] = mapped_column(BIT(1))
    bDEV_09: Mapped[Any] = mapped_column(BIT(1))
    nOrder: Mapped[int] = mapped_column(SmallInteger)
    TenantId: Mapped[int] = mapped_column(Integer)
    szCardName: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    szCardCaption: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    szMemo: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Syscardtype(Base):
    __tablename__ = 'syscardtype'
    __table_args__ = (
        Index('IX_SysCardType_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    Deposit: Mapped[int] = mapped_column(Integer)
    ExpirTime: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Syscoderule(Base):
    __tablename__ = 'syscoderule'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Code: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    CurrentNumber: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    RuleFormatJson: Mapped[Optional[str]] = mapped_column(TEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Syscoderuleseed(Base):
    __tablename__ = 'syscoderuleseed'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    SeedValue: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    CodeRuleId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Sysconfigbase(Base):
    __tablename__ = 'sysconfigbase'
    __table_args__ = (
        Index('IX_SysConfigBase_TenantId', 'TenantId'),
        Index('IX_SysConfigBase_TerminalId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ConfigType: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Content: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Sysconfiglog(Base):
    __tablename__ = 'sysconfiglog'
    __table_args__ = (
        Index('IX_SysConfigLog_TenantId', 'TenantId'),
        Index('IX_SysConfigLog_TerminalId', 'TerminalId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TerminalId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ConfigType: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Content: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Sysdataitem(Base):
    __tablename__ = 'sysdataitem'
    __table_args__ = (
        Index('IX_SysDataItem_Code', 'Code'),
        Index('IX_SysDataItem_ParentId', 'ParentId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(64))
    IsTree: Mapped[Any] = mapped_column(BIT(1))
    SortCode: Mapped[int] = mapped_column(Integer)
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ParentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Sysdataitemdetail(Base):
    __tablename__ = 'sysdataitemdetail'
    __table_args__ = (
        Index('IX_SysDataItemDetail_ItemCode', 'ItemCode'),
        Index('IX_SysDataItemDetail_ParentId', 'ParentId')
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    ItemId: Mapped[str] = mapped_column(VARCHAR(32))
    ItemCode: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(64))
    Value: Mapped[str] = mapped_column(VARCHAR(64))
    IsDefault: Mapped[Any] = mapped_column(BIT(1))
    SortCode: Mapped[int] = mapped_column(Integer)
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    QuickQuery: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    SimpleSpelling: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ParentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Sysdatalog(Base):
    __tablename__ = 'sysdatalog'
    __table_args__ = (
        Index('IX_SysDataLog_TenantId_CreationTime', 'TenantId', 'CreationTime'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    InsertType: Mapped[int] = mapped_column(Integer)
    IsOffLine: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    KeyValue: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    DBType: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    Business: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    SysName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ClientName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Description: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CreatorUserName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))


class Sysdepartment(Base):
    __tablename__ = 'sysdepartment'
    __table_args__ = (
        Index('IX_SysDepartment_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Code: Mapped[str] = mapped_column(VARCHAR(95))
    Name: Mapped[str] = mapped_column(VARCHAR(256))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ParentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Sysenumfield(Base):
    __tablename__ = 'sysenumfield'
    __table_args__ = (
        Index('IX_SysEnumField_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    FieldId: Mapped[int] = mapped_column(Integer)
    IsEdit: Mapped[Any] = mapped_column(BIT(1))
    IsShow: Mapped[Any] = mapped_column(BIT(1))
    IsSingleValue: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    FieldName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    FieldTrans: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Sysenumvalue(Base):
    __tablename__ = 'sysenumvalue'
    __table_args__ = (
        Index('IX_SysEnumValue_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    EnumValueId: Mapped[int] = mapped_column(Integer)
    DataType: Mapped[int] = mapped_column(Integer)
    EnumOrder: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    FieldName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Value: Mapped[Optional[int]] = mapped_column(Integer)
    StringValue: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    EnumTrans: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Sysenumvalue2(Base):
    __tablename__ = 'sysenumvalue2'
    __table_args__ = (
        Index('IX_SysEnumValue2_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    EnumValueId: Mapped[int] = mapped_column(Integer)
    FieldId: Mapped[int] = mapped_column(Integer)
    IsCanEdit: Mapped[Any] = mapped_column(BIT(1))
    Order: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    EnumValue: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    EnumTrans: Mapped[Optional[str]] = mapped_column(VARCHAR(500))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Sysfaceoffineoperationlog(Base):
    __tablename__ = 'sysfaceoffineoperationlog'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    OperationType: Mapped[int] = mapped_column(TINYINT)
    OperationItem: Mapped[int] = mapped_column(TINYINT)
    Result: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    GroupId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UserId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ErrorMessage: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    OperationMessage: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Sysfaceofflinefeature(Base):
    __tablename__ = 'sysfaceofflinefeature'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    FaceId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    UserId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    GroupId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    FaceToken: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Feature: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Image: Mapped[Optional[str]] = mapped_column(LONGTEXT)


class Sysfaceofflinegroup(Base):
    __tablename__ = 'sysfaceofflinegroup'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    GroupId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    GroupName: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Sysfaceofflineuser(Base):
    __tablename__ = 'sysfaceofflineuser'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    GroupId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UserId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    UserInfo: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Image: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Syslanguage(Base):
    __tablename__ = 'syslanguage'
    __table_args__ = (
        Index('IX_SysLanguage_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Key: Mapped[str] = mapped_column(VARCHAR(512))
    Order: Mapped[decimal.Decimal] = mapped_column(DECIMAL(65, 30))
    Category: Mapped[str] = mapped_column(VARCHAR(32))
    TargetCulture: Mapped[str] = mapped_column(VARCHAR(32))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    BaseValue: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    TargetValue: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    Source: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(32))


class Syslayertrans(Base):
    __tablename__ = 'syslayertrans'
    __table_args__ = (
        Index('IX_SysLayerTrans_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    IsShowBuilding: Mapped[Any] = mapped_column(BIT(1))
    IsShowFloor: Mapped[Any] = mapped_column(BIT(1))
    IsShowRoom: Mapped[Any] = mapped_column(BIT(1))
    IsSelected: Mapped[Any] = mapped_column(BIT(1))
    TenantId: Mapped[int] = mapped_column(Integer)
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Row: Mapped[Optional[str]] = mapped_column(VARCHAR(8))
    Column: Mapped[Optional[str]] = mapped_column(VARCHAR(8))
    Face: Mapped[Optional[str]] = mapped_column(VARCHAR(8))
    Layer: Mapped[Optional[str]] = mapped_column(VARCHAR(8))
    ShowMode: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    LayerSort: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ColumnSort: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Description: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Syslocation(Base):
    __tablename__ = 'syslocation'
    __table_args__ = (
        Index('IX_SysLocation_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    IsDefault: Mapped[Any] = mapped_column(BIT(1))
    LocationType: Mapped[int] = mapped_column(TINYINT)
    Longitude: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 6))
    Latitude: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 6))
    TenantId: Mapped[int] = mapped_column(Integer)
    IsForceSort: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ParentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Province: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    City: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    District: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Street: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Address: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CatalogSort: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    SortCode: Mapped[Optional[int]] = mapped_column(Integer)


class Sysmenu(Base):
    __tablename__ = 'sysmenu'

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Code: Mapped[str] = mapped_column(VARCHAR(32))
    Name: Mapped[str] = mapped_column(VARCHAR(32))
    IsExternal: Mapped[Any] = mapped_column(BIT(1))
    IsIframe: Mapped[Any] = mapped_column(BIT(1))
    IsAuthenticate: Mapped[Any] = mapped_column(BIT(1))
    SortCode: Mapped[int] = mapped_column(Integer)
    IsEnable: Mapped[Any] = mapped_column(BIT(1))
    SystemType: Mapped[int] = mapped_column(TINYINT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    PermissionName: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    Icon: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Route: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Parameters: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    FeatureDependency: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ParentId: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)


class Systasklist(Base):
    __tablename__ = 'systasklist'
    __table_args__ = (
        Index('IX_SysTaskList_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TaskType: Mapped[int] = mapped_column(TINYINT)
    Order: Mapped[int] = mapped_column(TINYINT)
    TaskStatus: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TaskName: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    CronExpression: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    AssemblyName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    ClassName: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    FilePath: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    OrderBy: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    LastExecTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    NextExecTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    PlanExecTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TaskParams: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Systenantconfig(Base):
    __tablename__ = 'systenantconfig'
    __table_args__ = (
        Index('IX_SysTenantConfig_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    System: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    BusinessRule: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Protocol: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    WeChat: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Alipay: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Baidu: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    QQWeiXiao: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Stat: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Task: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Points: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))


class Systenantextend(Base):
    __tablename__ = 'systenantextend'
    __table_args__ = (
        Index('IX_SysTenantExtend_TenantId', 'TenantId'),
    )

    Id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    TenantType: Mapped[int] = mapped_column(TINYINT)
    Level: Mapped[int] = mapped_column(TINYINT)
    TenantId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LibraryCode: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    Custom: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))
    Remark: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    RegistrationCode: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))


class Abpentitychanges(Base):
    __tablename__ = 'abpentitychanges'
    __table_args__ = (
        ForeignKeyConstraint(['EntityChangeSetId'], ['abpentitychangesets.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpEntityChanges_AbpEntityChangeSets_EntityChangeSetId'),
        Index('IX_AbpEntityChanges_EntityChangeSetId', 'EntityChangeSetId'),
        Index('IX_AbpEntityChanges_EntityTypeFullName_EntityId', 'EntityTypeFullName', 'EntityId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ChangeTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    ChangeType: Mapped[int] = mapped_column(TINYINT)
    EntityChangeSetId: Mapped[int] = mapped_column(BigInteger)
    EntityId: Mapped[Optional[str]] = mapped_column(VARCHAR(48))
    EntityTypeFullName: Mapped[Optional[str]] = mapped_column(VARCHAR(192))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)

    abpentitychangesets: Mapped['Abpentitychangesets'] = relationship('Abpentitychangesets', back_populates='abpentitychanges')
    abpentitypropertychanges: Mapped[List['Abpentitypropertychanges']] = relationship('Abpentitypropertychanges', back_populates='abpentitychanges')


class Abpfeatures(Base):
    __tablename__ = 'abpfeatures'
    __table_args__ = (
        ForeignKeyConstraint(['EditionId'], ['abpeditions.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpFeatures_AbpEditions_EditionId'),
        Index('IX_AbpFeatures_EditionId_Name', 'EditionId', 'Name'),
        Index('IX_AbpFeatures_TenantId_Name', 'TenantId', 'Name')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    Value: Mapped[str] = mapped_column(VARCHAR(2000))
    Discriminator: Mapped[str] = mapped_column(LONGTEXT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    EditionId: Mapped[Optional[int]] = mapped_column(Integer)

    abpeditions: Mapped[Optional['Abpeditions']] = relationship('Abpeditions', back_populates='abpfeatures')


class Abproles(Base):
    __tablename__ = 'abproles'
    __table_args__ = (
        ForeignKeyConstraint(['CreatorUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpRoles_AbpUsers_CreatorUserId'),
        ForeignKeyConstraint(['DeleterUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpRoles_AbpUsers_DeleterUserId'),
        ForeignKeyConstraint(['LastModifierUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpRoles_AbpUsers_LastModifierUserId'),
        Index('IX_AbpRoles_CreatorUserId', 'CreatorUserId'),
        Index('IX_AbpRoles_DeleterUserId', 'DeleterUserId'),
        Index('IX_AbpRoles_LastModifierUserId', 'LastModifierUserId'),
        Index('IX_AbpRoles_TenantId_NormalizedName', 'TenantId', 'NormalizedName')
    )

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Name: Mapped[str] = mapped_column(VARCHAR(32))
    DisplayName: Mapped[str] = mapped_column(VARCHAR(64))
    IsStatic: Mapped[Any] = mapped_column(BIT(1))
    IsDefault: Mapped[Any] = mapped_column(BIT(1))
    NormalizedName: Mapped[str] = mapped_column(VARCHAR(32))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ConcurrencyStamp: Mapped[Optional[str]] = mapped_column(VARCHAR(128))

    abpusers: Mapped[Optional['Abpusers']] = relationship('Abpusers', foreign_keys=[CreatorUserId], back_populates='abproles')
    abpusers_: Mapped[Optional['Abpusers']] = relationship('Abpusers', foreign_keys=[DeleterUserId], back_populates='abproles_')
    abpusers1: Mapped[Optional['Abpusers']] = relationship('Abpusers', foreign_keys=[LastModifierUserId], back_populates='abproles1')
    abppermissions: Mapped[List['Abppermissions']] = relationship('Abppermissions', back_populates='abproles')
    abproleclaims: Mapped[List['Abproleclaims']] = relationship('Abproleclaims', back_populates='abproles')


class Abpsettings(Base):
    __tablename__ = 'abpsettings'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpSettings_AbpUsers_UserId'),
        Index('IX_AbpSettings_TenantId_Name_UserId', 'TenantId', 'Name', 'UserId', unique=True),
        Index('IX_AbpSettings_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Name: Mapped[str] = mapped_column(VARCHAR(256))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    Value: Mapped[Optional[str]] = mapped_column(VARCHAR(2000))

    abpusers: Mapped[Optional['Abpusers']] = relationship('Abpusers', back_populates='abpsettings')


class Abptenants(Base):
    __tablename__ = 'abptenants'
    __table_args__ = (
        ForeignKeyConstraint(['CreatorUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpTenants_AbpUsers_CreatorUserId'),
        ForeignKeyConstraint(['DeleterUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpTenants_AbpUsers_DeleterUserId'),
        ForeignKeyConstraint(['EditionId'], ['abpeditions.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpTenants_AbpEditions_EditionId'),
        ForeignKeyConstraint(['LastModifierUserId'], ['abpusers.Id'], ondelete='RESTRICT', onupdate='RESTRICT', name='FK_AbpTenants_AbpUsers_LastModifierUserId'),
        Index('IX_AbpTenants_CreationTime', 'CreationTime'),
        Index('IX_AbpTenants_CreatorUserId', 'CreatorUserId'),
        Index('IX_AbpTenants_DeleterUserId', 'DeleterUserId'),
        Index('IX_AbpTenants_EditionId', 'EditionId'),
        Index('IX_AbpTenants_LastModifierUserId', 'LastModifierUserId'),
        Index('IX_AbpTenants_SubscriptionEndDateUtc', 'SubscriptionEndDateUtc'),
        Index('IX_AbpTenants_TenancyName', 'TenancyName')
    )

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    TenancyName: Mapped[str] = mapped_column(VARCHAR(64))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    IsActive: Mapped[Any] = mapped_column(BIT(1))
    IsInTrialPeriod: Mapped[Any] = mapped_column(BIT(1))
    SubscriptionPaymentType: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    ConnectionString: Mapped[Optional[str]] = mapped_column(VARCHAR(1024))
    EditionId: Mapped[Optional[int]] = mapped_column(Integer)
    SubscriptionEndDateUtc: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    CustomCssId: Mapped[Optional[str]] = mapped_column(CHAR(36))
    LogoId: Mapped[Optional[str]] = mapped_column(CHAR(36))
    LogoFileType: Mapped[Optional[str]] = mapped_column(VARCHAR(64))

    abpusers: Mapped[Optional['Abpusers']] = relationship('Abpusers', foreign_keys=[CreatorUserId], back_populates='abptenants')
    abpusers_: Mapped[Optional['Abpusers']] = relationship('Abpusers', foreign_keys=[DeleterUserId], back_populates='abptenants_')
    abpeditions: Mapped[Optional['Abpeditions']] = relationship('Abpeditions', back_populates='abptenants')
    abpusers1: Mapped[Optional['Abpusers']] = relationship('Abpusers', foreign_keys=[LastModifierUserId], back_populates='abptenants1')


class Abpuserclaims(Base):
    __tablename__ = 'abpuserclaims'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['abpusers.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpUserClaims_AbpUsers_UserId'),
        Index('IX_AbpUserClaims_TenantId_ClaimType', 'TenantId', 'ClaimType'),
        Index('IX_AbpUserClaims_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    UserId: Mapped[int] = mapped_column(BigInteger)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ClaimType: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ClaimValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)

    abpusers: Mapped['Abpusers'] = relationship('Abpusers', back_populates='abpuserclaims')


class Abpuserlogins(Base):
    __tablename__ = 'abpuserlogins'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['abpusers.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpUserLogins_AbpUsers_UserId'),
        Index('IX_AbpUserLogins_TenantId_LoginProvider_ProviderKey', 'TenantId', 'LoginProvider', 'ProviderKey'),
        Index('IX_AbpUserLogins_TenantId_UserId', 'TenantId', 'UserId'),
        Index('IX_AbpUserLogins_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    UserId: Mapped[int] = mapped_column(BigInteger)
    LoginProvider: Mapped[str] = mapped_column(VARCHAR(128))
    ProviderKey: Mapped[str] = mapped_column(VARCHAR(256))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)

    abpusers: Mapped['Abpusers'] = relationship('Abpusers', back_populates='abpuserlogins')


class Abpuserorganizationunits(Base):
    __tablename__ = 'abpuserorganizationunits'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['abpusers.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpUserOrganizationUnits_AbpUsers_UserId'),
        Index('IX_AbpUserOrganizationUnits_TenantId_OrganizationUnitId', 'TenantId', 'OrganizationUnitId'),
        Index('IX_AbpUserOrganizationUnits_TenantId_UserId', 'TenantId', 'UserId'),
        Index('IX_AbpUserOrganizationUnits_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    UserId: Mapped[int] = mapped_column(BigInteger)
    OrganizationUnitId: Mapped[int] = mapped_column(BigInteger)
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)

    abpusers: Mapped['Abpusers'] = relationship('Abpusers', back_populates='abpuserorganizationunits')


class Abpuserroles(Base):
    __tablename__ = 'abpuserroles'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['abpusers.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpUserRoles_AbpUsers_UserId'),
        Index('IX_AbpUserRoles_TenantId_RoleId', 'TenantId', 'RoleId'),
        Index('IX_AbpUserRoles_TenantId_UserId', 'TenantId', 'UserId'),
        Index('IX_AbpUserRoles_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    UserId: Mapped[int] = mapped_column(BigInteger)
    RoleId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)

    abpusers: Mapped['Abpusers'] = relationship('Abpusers', back_populates='abpuserroles')


class Abpusertokens(Base):
    __tablename__ = 'abpusertokens'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['abpusers.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpUserTokens_AbpUsers_UserId'),
        Index('IX_AbpUserTokens_TenantId_UserId', 'TenantId', 'UserId'),
        Index('IX_AbpUserTokens_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    UserId: Mapped[int] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    LoginProvider: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Name: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    Value: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    ExpireDate: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))

    abpusers: Mapped['Abpusers'] = relationship('Abpusers', back_populates='abpusertokens')


class Appsubscriptionpayments(Base):
    __tablename__ = 'appsubscriptionpayments'
    __table_args__ = (
        ForeignKeyConstraint(['EditionId'], ['abpeditions.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AppSubscriptionPayments_AbpEditions_EditionId'),
        Index('IX_AppSubscriptionPayments_EditionId', 'EditionId'),
        Index('IX_AppSubscriptionPayments_ExternalPaymentId_Gateway', 'ExternalPaymentId', 'Gateway'),
        Index('IX_AppSubscriptionPayments_Status_CreationTime', 'Status', 'CreationTime')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    IsDeleted: Mapped[Any] = mapped_column(BIT(1))
    Gateway: Mapped[int] = mapped_column(Integer)
    Amount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(65, 30))
    Status: Mapped[int] = mapped_column(Integer)
    EditionId: Mapped[int] = mapped_column(Integer)
    TenantId: Mapped[int] = mapped_column(Integer)
    DayCount: Mapped[int] = mapped_column(Integer)
    IsRecurring: Mapped[Any] = mapped_column(BIT(1))
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    LastModificationTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    LastModifierUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeleterUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    DeletionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    Description: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    PaymentPeriodType: Mapped[Optional[int]] = mapped_column(Integer)
    ExternalPaymentId: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    InvoiceNo: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    SuccessUrl: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    ErrorUrl: Mapped[Optional[str]] = mapped_column(LONGTEXT)

    abpeditions: Mapped['Abpeditions'] = relationship('Abpeditions', back_populates='appsubscriptionpayments')


class Libailibrarainbaseinfoitem(Base):
    __tablename__ = 'libailibrarainbaseinfoitem'
    __table_args__ = (
        ForeignKeyConstraint(['BaseInfoId'], ['libailibrarainbaseinfo.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_LibAiLibrarainBaseInfoItem_LibAiLibrarainBaseInfo_BaseInfoId'),
        Index('IX_LibAiLibrarainBaseInfoItem_BaseInfoId', 'BaseInfoId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    Name: Mapped[str] = mapped_column(VARCHAR(50))
    Content: Mapped[str] = mapped_column(VARCHAR(1024))
    BaseInfoId: Mapped[int] = mapped_column(BigInteger)

    libailibrarainbaseinfo: Mapped['Libailibrarainbaseinfo'] = relationship('Libailibrarainbaseinfo', back_populates='libailibrarainbaseinfoitem')


class OwenUser(Base):
    __tablename__ = 'owen_user'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['owen_role.id'], name='fk_owen_user_role'),
        Index('fk_owen_user_role', 'role_id'),
        Index('uni_owen_user_username', 'username', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    password: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    role_id: Mapped[Optional[int]] = mapped_column(BIGINT)

    role: Mapped[Optional['OwenRole']] = relationship('OwenRole', back_populates='owen_user')


class Abpentitypropertychanges(Base):
    __tablename__ = 'abpentitypropertychanges'
    __table_args__ = (
        ForeignKeyConstraint(['EntityChangeId'], ['abpentitychanges.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpEntityPropertyChanges_AbpEntityChanges_EntityChangeId'),
        Index('IX_AbpEntityPropertyChanges_EntityChangeId', 'EntityChangeId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    EntityChangeId: Mapped[int] = mapped_column(BigInteger)
    NewValue: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    OriginalValue: Mapped[Optional[str]] = mapped_column(VARCHAR(512))
    PropertyName: Mapped[Optional[str]] = mapped_column(VARCHAR(96))
    PropertyTypeFullName: Mapped[Optional[str]] = mapped_column(VARCHAR(192))
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)

    abpentitychanges: Mapped['Abpentitychanges'] = relationship('Abpentitychanges', back_populates='abpentitypropertychanges')


class Abppermissions(Base):
    __tablename__ = 'abppermissions'
    __table_args__ = (
        ForeignKeyConstraint(['RoleId'], ['abproles.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpPermissions_AbpRoles_RoleId'),
        ForeignKeyConstraint(['UserId'], ['abpusers.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpPermissions_AbpUsers_UserId'),
        Index('IX_AbpPermissions_RoleId', 'RoleId'),
        Index('IX_AbpPermissions_TenantId_Name', 'TenantId', 'Name'),
        Index('IX_AbpPermissions_UserId', 'UserId')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    Name: Mapped[str] = mapped_column(VARCHAR(128))
    IsGranted: Mapped[Any] = mapped_column(BIT(1))
    Discriminator: Mapped[str] = mapped_column(LONGTEXT)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    RoleId: Mapped[Optional[int]] = mapped_column(Integer)
    UserId: Mapped[Optional[int]] = mapped_column(BigInteger)

    abproles: Mapped[Optional['Abproles']] = relationship('Abproles', back_populates='abppermissions')
    abpusers: Mapped[Optional['Abpusers']] = relationship('Abpusers', back_populates='abppermissions')


class Abproleclaims(Base):
    __tablename__ = 'abproleclaims'
    __table_args__ = (
        ForeignKeyConstraint(['RoleId'], ['abproles.Id'], ondelete='CASCADE', onupdate='RESTRICT', name='FK_AbpRoleClaims_AbpRoles_RoleId'),
        Index('IX_AbpRoleClaims_RoleId', 'RoleId'),
        Index('IX_AbpRoleClaims_TenantId_ClaimType', 'TenantId', 'ClaimType')
    )

    Id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CreationTime: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6))
    RoleId: Mapped[int] = mapped_column(Integer)
    CreatorUserId: Mapped[Optional[int]] = mapped_column(BigInteger)
    TenantId: Mapped[Optional[int]] = mapped_column(Integer)
    ClaimType: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    ClaimValue: Mapped[Optional[str]] = mapped_column(LONGTEXT)

    abproles: Mapped['Abproles'] = relationship('Abproles', back_populates='abproleclaims')
