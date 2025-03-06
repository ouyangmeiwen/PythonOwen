#pip install aiomysql
from sqlalchemy import create_engine, Column, Integer, String, func, text, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import NoResultFound
from typing import Type, TypeVar, List, Optional, Any, Tuple
from app.dbmodel.base_model import Base
from sqlalchemy.future import select

# 定义泛型 T 表示任意 SQLAlchemy 模型类
T = TypeVar("T", bound=Base)  # type: ignore

class DatabaseAsy:
    """sqlalchemy异步数据仓储"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_async_engine(self.db_url, pool_size=10, max_overflow=20, future=True)
        # Use asyncmy instead of pymysql
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
    
    async def create_tables(self, models: Optional[List[Type[Base]]] = None):  # type: ignore
        """创建所有数据库表，或只创建指定的表"""
        async with self.engine.begin() as conn:
            if models:
                tables_to_create = {model.__tablename__: Base.metadata.tables[model.__tablename__] for model in models}
                await conn.run_sync(Base.metadata.create_all, tables=tables_to_create.values())
            else:
                await conn.run_sync(Base.metadata.create_all)

    async def add(self, obj: T) -> None:
        """添加任意模型对象到数据库"""
        async with self.Session() as session:
            session.add(obj)
            await session.commit()

    async def add_bulk(self, objs: List[T]) -> None:
        """批量添加模型对象到数据库"""
        async with self.Session() as session:
            await session.bulk_save_objects(objs)
            await session.commit()

    async def add_bulk_transaction(self, objs: List[T]) -> None:
        """批量插入模型对象，以事务方式处理。"""
        async with self.Session() as session:
            try:
                await session.bulk_save_objects(objs)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    async def update(self, obj: T, **kwargs) -> T:
        """更新对象的指定字段"""
        async with self.Session() as session:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            await session.commit()
        return obj

    async def update_bulk(self, model: Type[T], updates: List[dict]) -> None:
        """批量更新模型对象"""
        async with self.Session() as session:
            await session.bulk_update_mappings(model, updates)
            await session.commit()

    async def update_bulk_transaction(self, model: Type[T], updates: List[dict]) -> None:
        """批量更新模型对象，以事务方式处理。"""
        async with self.Session() as session:
            try:
                await session.bulk_update_mappings(model, updates)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    async def delete(self, obj: T) -> None:
        """删除指定的对象"""
        async with self.Session() as session:
            await session.delete(obj)
            await session.commit()

    async def delete_bulk(self, model: Type[T], ids: List[int]) -> None:
        """批量删除模型对象"""
        async with self.Session() as session:
            await session.query(model).filter(model.id.in_(ids)).delete(synchronize_session='fetch')
            await session.commit()

    async def delete_bulk_transaction(self, model: Type[T], ids: List[int]) -> None:
        """批量删除模型对象，以事务方式处理。"""
        async with self.Session() as session:
            try:
                await session.query(model).filter(model.id.in_(ids)).delete(synchronize_session='fetch')
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    async def exists(self, model: Type[T], *filters, **kwargs) -> bool:
        """检查记录是否存在"""
        async with self.Session() as session:
            query = select(model)
            for attr, value in kwargs.items():
                query = query.filter(getattr(model, attr) == value)
            if filters:
                query = query.filter(*filters)
            result = await session.execute(query)
            return result.scalar() is not None

    async def count(self, model: Type[T], *filters, **kwargs) -> int:
        """统计记录总数或满足条件的记录数"""
        async with self.Session() as session:
            query = select(model)
            for attr, value in kwargs.items():
                query = query.filter(getattr(model, attr) == value)
            if filters:
                query = query.filter(*filters)
            result = await session.execute(query)
            return result.scalar()

    async def aggregate(self, model: Type[T], field: str, agg_func: str, *filters, **kwargs) -> Optional[Any]:
        """对指定字段进行聚合计算"""
        async with self.Session() as session:
            query = select(getattr(func, agg_func)(getattr(model, field)))
            for attr, value in kwargs.items():
                query = query.filter(getattr(model, attr) == value)
            if filters:
                query = query.filter(*filters)
            result = await session.execute(query)
            return result.scalar()

    async def get_columns(self, model: Type[T], columns: List[str], *filters, **kwargs) -> List[dict]:
        """查询指定列的记录"""
        async with self.Session() as session:
            query = select(*(getattr(model, col) for col in columns))
            for attr, value in kwargs.items():
                query = query.filter(getattr(model, attr) == value)
            if filters:
                query = query.filter(*filters)
            result = await session.execute(query)
            return [dict(zip(columns, row)) for row in result.all()]

    async def get_all(self, model: Type[T]) -> List[T]:
        """查询某模型类的所有记录"""
        async with self.Session() as session:
            query = select(model)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_id(self, model: Type[T], obj_id: int) -> Optional[T]:
        """通过 ID 查询单个记录"""
        async with self.Session() as session:
            try:
                query = select(model).filter(model.id == obj_id)
                result = await session.execute(query)
                return result.scalar()
            except NoResultFound:
                return None

    async def get_by_name(self, model: Type[T], username: str) -> Optional[T]:
        """通过名称查询单个记录"""
        async with self.Session() as session:
            try:
                query = select(model).filter(model.username == username)
                result = await session.execute(query)
                return result.scalar()
            except NoResultFound:
                return None

    async def first_or_default(self, model: Type[T], *filters, **kwargs) -> Optional[T]:
        """根据任意条件查询记录, 返回单条记录"""
        result_lst = await self.where_many(model, *filters, **kwargs)
        return result_lst[0] if result_lst else None

    async def where_many(self, model: Type[T], *filters, **kwargs) -> List[T]:
        """根据条件查询记录，支持复杂查询"""
        async with self.Session() as session:
            query = select(model)
            for attr, value in kwargs.items():
                query = query.filter(getattr(model, attr) == value)
            if filters:
                query = query.filter(*filters)
            result = await session.execute(query)
            return result.scalars().all()

    async def where_bypage(self, model: Type[T], *filters, page: int = 1, page_size: int = 10, order_by: Optional[str] = None, ascending: bool = True, **kwargs) -> Tuple[List[T], int]:
        """分页查询记录"""
        async with self.Session() as session:
            query = select(model)
            for attr, value in kwargs.items():
                query = query.filter(getattr(model, attr) == value)
            if filters:
                query = query.filter(*filters)
            if order_by:
                if ascending:
                    query = query.order_by(asc(order_by))
                else:
                    query = query.order_by(desc(order_by))
            total_count = await session.execute(select(func.count()).select_from(query))
            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)
            items = await session.execute(query)
            return items.scalars().all(), total_count.scalar()

    async def execute_sql(self, sql: str, params: dict = None) -> Any:
        """执行原生 SQL 语句"""
        async with self.Session() as session:
            result = await session.execute(text(sql), params or {})
            await session.commit()
            return result

    async def execute_sql_batch(self, sql_list: List[str], params_list: Optional[List[dict]] = None) -> None:
        """批量执行原生 SQL 语句"""
        async with self.Session() as session:
            try:
                for i, sql in enumerate(sql_list):
                    params = params_list[i] if params_list else None
                    await session.execute(text(sql), params or {})
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    async def begin_transaction(self):
        """开启事务"""
        async with self.Session() as session:
            await session.begin()

    async def commit_transaction(self):
        """提交事务"""
        async with self.Session() as session:
            await session.commit()

    async def rollback_transaction(self):
        """回滚事务"""
        async with self.Session() as session:
            await session.rollback()

    async def get_session(self):
        """获取当前会话"""
        return self.Session()

    async def close(self):
        """关闭数据库会话"""
        async with self.Session() as session:
            await session.close()
