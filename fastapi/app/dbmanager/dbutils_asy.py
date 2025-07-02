import logging
from typing import Type, TypeVar, List, Optional, Any, Tuple, AsyncGenerator
from sqlalchemy import func, text, asc, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.dbmodel.base_model import Base
from contextlib import asynccontextmanager

T = TypeVar("T", bound=Base)
logger = logging.getLogger(__name__)

class DatabaseAsy:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_async_engine(
            self.db_url, pool_size=10, max_overflow=20, pool_pre_ping=True, future=True
        )
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self._manual_session: Optional[AsyncSession] = None  # 手动事务专用会话

    async def begin_transaction(self):
        if self._manual_session is not None:
            logger.warning("事务已开启，不能重复开启")
            return
        self._manual_session = self.Session()
        await self._manual_session.begin()
        logger.debug("手动事务已开启")

    async def commit_transaction(self):
        if not self._manual_session:
            logger.warning("没有手动事务可提交")
            return
        try:
            await self._manual_session.commit()
            logger.debug("手动事务提交成功")
        except Exception as e:
            logger.error(f"提交事务失败: {e}")
            raise
        finally:
            await self._manual_session.close()
            self._manual_session = None

    async def rollback_transaction(self):
        if not self._manual_session:
            logger.warning("没有手动事务可回滚")
            return
        try:
            await self._manual_session.rollback()
            logger.debug("手动事务回滚成功")
        except Exception as e:
            logger.error(f"回滚事务失败: {e}")
            raise
        finally:
            await self._manual_session.close()
            self._manual_session = None

    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        """
        优先使用手动事务会话，否则新建临时会话。
        自动提交/回滚，仅针对临时会话。
        """
        if self._manual_session:
            # 手动事务已开启，复用手动会话，不自动提交
            yield self._manual_session
        else:
            async with self.Session() as session:
                try:
                    yield session
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise

    async def _get_session(self) -> AsyncSession:
        """
        内部调用获取当前会话，优先手动事务会话
        """
        if self._manual_session:
            return self._manual_session
        else:
            return self.Session()

    async def create_tables(self, models: Optional[List[Type[Base]]] = None):
        async with self.engine.begin() as conn:
            if models:
                tables = {m.__tablename__: Base.metadata.tables[m.__tablename__] for m in models}
                await conn.run_sync(Base.metadata.create_all, tables=tables.values())
            else:
                await conn.run_sync(Base.metadata.create_all)

    async def add(self, obj: T) -> None:
        async with self.session_scope() as session:
            session.add(obj)

    async def add_bulk(self, objs: List[T]) -> None:
        async with self.session_scope() as session:
            session.add_all(objs)

    async def add_bulk_transaction(self, objs: List[T]) -> None:
        await self.add_bulk(objs)

    async def update(self, obj: T, **kwargs) -> T:
        async with self.session_scope() as session:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
        return obj

    async def update_bulk(self, model: Type[T], updates: List[dict]) -> None:
        async with self.session_scope() as session:
            await session.bulk_update_mappings(model, updates)

    async def update_bulk_transaction(self, model: Type[T], updates: List[dict]) -> None:
        await self.update_bulk(model, updates)

    async def delete(self, obj: T) -> None:
        async with self.session_scope() as session:
            await session.delete(obj)

    async def delete_bulk(self, model: Type[T], ids: List[int]) -> None:
        async with self.session_scope() as session:
            stmt = delete(model).where(model.id.in_(ids))
            await session.execute(stmt)

    async def delete_bulk_transaction(self, model: Type[T], ids: List[int]) -> None:
        await self.delete_bulk(model, ids)

    async def exists(self, model: Type[T], *filters, **kwargs) -> bool:
        async with self.session_scope() as session:
            query = select(model)
            for attr, value in kwargs.items():
                query = query.where(getattr(model, attr) == value)
            if filters:
                query = query.where(*filters)
            result = await session.execute(query)
            return result.scalar() is not None

    async def count(self, model: Type[T], *filters, **kwargs) -> int:
        async with self.session_scope() as session:
            query = select(func.count()).select_from(model)
            for attr, value in kwargs.items():
                query = query.where(getattr(model, attr) == value)
            if filters:
                query = query.where(*filters)
            result = await session.execute(query)
            return result.scalar()

    async def aggregate(self, model: Type[T], field: str, agg_func: str, *filters, **kwargs) -> Optional[Any]:
        async with self.session_scope() as session:
            query = select(getattr(func, agg_func)(getattr(model, field)))
            for attr, value in kwargs.items():
                query = query.where(getattr(model, attr) == value)
            if filters:
                query = query.where(*filters)
            result = await session.execute(query)
            return result.scalar()

    async def get_columns(self, model: Type[T], columns: List[str], *filters, **kwargs) -> List[dict]:
        async with self.session_scope() as session:
            query = select(*(getattr(model, col) for col in columns))
            for attr, value in kwargs.items():
                query = query.where(getattr(model, attr) == value)
            if filters:
                query = query.where(*filters)
            result = await session.execute(query)
            return [dict(row) for row in result.mappings().all()]

    async def get_all(self, model: Type[T]) -> List[T]:
        async with self.session_scope() as session:
            result = await session.execute(select(model))
            return result.scalars().all()

    async def get_by_id(self, model: Type[T], obj_id: int) -> Optional[T]:
        async with self.session_scope() as session:
            result = await session.execute(select(model).where(model.id == obj_id))
            return result.scalar()

    async def get_by_name(self, model: Type[T], username: str) -> Optional[T]:
        async with self.session_scope() as session:
            result = await session.execute(select(model).where(model.username == username))
            return result.scalar()

    async def first_or_default(self, model: Type[T], *filters, **kwargs) -> Optional[T]:
        result = await self.where_many(model, *filters, **kwargs)
        return result[0] if result else None

    async def where_many(self, model: Type[T], *filters, **kwargs) -> List[T]:
        async with self.session_scope() as session:
            query = select(model)
            for attr, value in kwargs.items():
                query = query.where(getattr(model, attr) == value)
            if filters:
                query = query.where(*filters)
            result = await session.execute(query)
            return result.scalars().all()

    async def where_bypage(
        self,
        model: Type[T],
        *filters,
        page: int = 1,
        page_size: int = 10,
        order_by: Optional[str] = None,
        ascending: bool = True,
        **kwargs
    ) -> Tuple[List[T], int]:
        async with self.session_scope() as session:
            base_query = select(model)
            for attr, value in kwargs.items():
                base_query = base_query.where(getattr(model, attr) == value)
            if filters:
                base_query = base_query.where(*filters)

            count_query = select(func.count()).select_from(base_query.subquery())
            total_result = await session.execute(count_query)
            total_count = total_result.scalar()

            if order_by:
                order_col = asc(order_by) if ascending else desc(order_by)
                base_query = base_query.order_by(order_col)

            base_query = base_query.offset((page - 1) * page_size).limit(page_size)
            items = await session.execute(base_query)
            return items.scalars().all(), total_count

    async def execute_sql(self, sql: str, params: dict = None) -> Any:
        async with self.session_scope() as session:
            result = await session.execute(text(sql), params or {})
            return result

    async def execute_sql_batch(self, sql_list: List[str], params_list: Optional[List[dict]] = None) -> None:
        async with self.session_scope() as session:
            for i, sql in enumerate(sql_list):
                params = params_list[i] if params_list else {}
                await session.execute(text(sql), params)

    async def get_session(self):
        """
        外部可直接获取会话（不自动提交，使用者自行管理事务）
        注意：使用后需手动关闭
        """
        return self.Session()

    async def close(self):
        await self.engine.dispose()
