import logging

from typing import (
    Type,
    TypeVar,
    List,
    Optional,
    Any,
    Tuple,
    AsyncGenerator
)

from sqlalchemy import (
    func,
    text,
    asc,
    desc,
    delete
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)

from sqlalchemy.orm import sessionmaker

from sqlalchemy.future import select

from app.dbmodel.base_model import Base

from contextlib import asynccontextmanager

from contextvars import ContextVar



T = TypeVar(
    "T",
    bound=Base
)


logger = logging.getLogger(__name__)



# 每个协程独立事务Session
_manual_session_ctx: ContextVar[
    Optional[AsyncSession]
] = ContextVar(
    "_manual_session_ctx",
    default=None
)



class DatabaseAsy:


    def __init__(
        self,
        db_url: str
    ):

        self.db_url = db_url


        self.engine = create_async_engine(
            self.db_url,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            future=True
        )


        self.Session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )



    # ===============================
    # 事务
    # ===============================


    async def begin_transaction(self):

        session = _manual_session_ctx.get()


        if session:

            logger.warning(
                "事务已开启，不能重复开启"
            )

            return



        session = self.Session()


        await session.begin()


        token = _manual_session_ctx.set(
        session
    )


        session.info["context_token"] = token


        logger.debug(
            "手动事务已开启"
        )



    async def commit_transaction(self):

        session = _manual_session_ctx.get()


        if not session:

            logger.warning(
                "没有手动事务可提交"
            )

            return



        try:

            await session.flush()
            await session.commit()

            logger.debug(
                "手动事务提交成功"
            )


        except Exception as e:

            logger.error(
                f"提交事务失败:{e}"
            )

            raise


        finally:

            await session.close()

            token = session.info.get(
        "context_token"
    )
            if token:
                _manual_session_ctx.reset(
                    token
            )



    async def rollback_transaction(self):

        session = _manual_session_ctx.get()


        if not session:

            logger.warning(
                "没有手动事务可回滚"
            )

            return



        try:

            await session.rollback()


            logger.debug(
                "手动事务回滚成功"
            )


        except Exception as e:

            logger.error(
                f"回滚事务失败:{e}"
            )

            raise


        finally:

            await session.close()


            token = session.info.get(
                "context_token"
            )


            if token:

                _manual_session_ctx.reset(
                    token
                )



    # ===============================
    # Session 生命周期
    # ===============================


    @asynccontextmanager
    async def session_scope(
        self
    ) -> AsyncGenerator[
        AsyncSession,
        None
    ]:


        manual = _manual_session_ctx.get()



        if manual:


            # 外部事务，不自动提交

            yield manual



        else:


            async with self.Session() as session:


                try:

                    yield session

                    await session.flush()

                    await session.commit()

                except Exception:

                    await session.rollback()

                    raise




    async def _create_session(
        self
    ) -> AsyncSession:


        session = _manual_session_ctx.get()


        if session:

            return session



        return self.Session()

    async def close_session(
        self,
        session
    ):
        if session:
            await session.close()

    # ===============================
    # 创建表
    # ===============================


    async def create_tables(
        self,
        models: Optional[
            List[Type[Base]]
        ] = None
    ):


        async with self.engine.begin() as conn:


            if models:


                tables = {
                    m.__tablename__:
                    Base.metadata.tables[
                        m.__tablename__
                    ]

                    for m in models
                }


                await conn.run_sync(
                    Base.metadata.create_all,
                    tables=tables.values()
                )


            else:


                await conn.run_sync(
                    Base.metadata.create_all
                )



    # ===============================
    # 新增
    # ===============================


    async def add(
        self,
        obj:T
    )->None:


        async with self.session_scope() as session:

            session.add(obj)
            await session.flush()


    async def add_bulk(
        self,
        objs:List[T]
    )->None:


        async with self.session_scope() as session:

            session.add_all(objs)



    async def add_bulk_transaction(
        self,
        objs:List[T]
    )->None:


        await self.add_bulk(
            objs
        )



    # ===============================
    # 更新
    # ===============================


    async def update(
        self,
        obj:T,
        **kwargs
    )->T:


        async with self.session_scope() as session:


            db_obj = await session.merge(
                obj
            )


            for key,value in kwargs.items():


                if hasattr(
                    db_obj,
                    key
                ):


                    setattr(
                        db_obj,
                        key,
                        value
                    )


        return db_obj



    async def update_bulk(
        self,
        model:Type[T],
        updates:List[dict]
    )->None:


        async with self.session_scope() as session:


            await session.run_sync(
                lambda s:
                s.bulk_update_mappings(
                    model,
                    updates
                )
            )



    async def update_bulk_transaction(
        self,
        model:Type[T],
        updates:List[dict]
    )->None:


        await self.update_bulk(
            model,
            updates
        )



    # ===============================
    # 删除
    # ===============================


    async def delete(
        self,
        obj:T
    )->None:


        async with self.session_scope() as session:

            await session.delete(
                obj
            )



    async def delete_bulk(
        self,
        model:Type[T],
        ids:List[int]
    )->None:


        async with self.session_scope() as session:


            stmt = delete(model).where(
                model.id.in_(ids)
            )
            await session.execute(
                stmt
            )


    async def delete_bulk_transaction(
        self,
        model:Type[T],
        ids:List[int]
    )->None:

        await self.delete_bulk(
            model,
            ids
        )



    # ===============================
    # 是否存在
    # ===============================


    async def exists(
    self,
    model:Type[T],
    *filters,
    **kwargs
)->bool:

        async with self.session_scope() as session:

            query = (
                select(1)
                .select_from(model)
                .limit(1)
            )


            for attr,value in kwargs.items():

                query = query.where(
                    getattr(model,attr)==value
                )


            if filters:

                query=query.where(
                    *filters
                )


            result = await session.execute(query)


            return result.first() is not None


    # ===============================
    # 数量
    # ===============================


    async def count(
        self,
        model:Type[T],
        *filters,
        **kwargs
    )->int:


        async with self.session_scope() as session:


            query = select(
                func.count()
            ).select_from(
                model
            )


            for attr,value in kwargs.items():

                query = query.where(
                    getattr(model,attr) == value
                )



            if filters:

                query = query.where(
                    *filters
                )



            result = await session.execute(
                query
            )


            return result.scalar()



    # ===============================
    # 聚合
    # ===============================


    async def aggregate(
        self,
        model:Type[T],
        field:str,
        agg_func:str,
        *filters,
        **kwargs
    )->Optional[Any]:


        async with self.session_scope() as session:


            query = select(
                getattr(
                    func,
                    agg_func
                )(
                    getattr(
                        model,
                        field
                    )
                )
            )


            for attr,value in kwargs.items():

                query = query.where(
                    getattr(model,attr)==value
                )



            if filters:

                query=query.where(
                    *filters
                )



            result = await session.execute(
                query
            )


            return result.scalar()



    # ===============================
    # 指定字段查询
    # ===============================


    async def get_columns(
        self,
        model:Type[T],
        columns:List[str],
        *filters,
        **kwargs
    )->List[dict]:


        async with self.session_scope() as session:


            query = select(
                *[
                    getattr(model,col)
                    for col in columns
                ]
            )



            for attr,value in kwargs.items():

                query=query.where(
                    getattr(model,attr)==value
                )



            if filters:

                query=query.where(
                    *filters
                )



            result = await session.execute(
                query
            )


            return list(
                result.mappings().all()
            )



    # ===============================
    # 查询全部
    # ===============================


    async def get_all(
        self,
        model:Type[T]
    )->List[T]:


        async with self.session_scope() as session:


            result = await session.execute(
                select(model)
            )


            return result.scalars().all()



    async def get_by_id(
        self,
        model:Type[T],
        obj_id:int
    )->Optional[T]:


        async with self.session_scope() as session:


             return await session.get(
                    model,
                    obj_id
                )



    async def get_by_name(
        self,
        model:Type[T],
        username:str
    )->Optional[T]:


        async with self.session_scope() as session:


            result = await session.execute(
                select(model)
                .where(
                    model.username == username
                )
            )


            return result.scalar()



    async def first_or_default(
        self,
        model:Type[T],
        *filters,
        **kwargs
    )->Optional[T]:


        result = await self.where_many(
            model,
            *filters,
            **kwargs
        )


        return result[0] if result else None



    async def where_many(
        self,
        model:Type[T],
        *filters,
        **kwargs
    )->List[T]:


        async with self.session_scope() as session:


            query = select(model)



            for attr,value in kwargs.items():

                query=query.where(
                    getattr(model,attr)==value
                )



            if filters:

                query=query.where(
                    *filters
                )



            result = await session.execute(
                query
            )


            return result.scalars().all()



    # ===============================
    # 分页
    # ===============================


    async def where_bypage(
        self,
        model:Type[T],
        *filters,
        page:int=1,
        page_size:int=10,
        order_by:Optional[str]=None,
        ascending:bool=True,
        **kwargs
    )->Tuple[List[T],int]:


        async with self.session_scope() as session:


            query = select(model)



            for attr,value in kwargs.items():

                query=query.where(
                    getattr(model,attr)==value
                )



            if filters:

                query=query.where(
                    *filters
                )



            count_query = select(
                func.count()
            ).select_from(
                query.subquery()
            )


            total_result = await session.execute(
                count_query
            )


            total_count = total_result.scalar()



            if order_by:


                order_col = getattr(
                    model,
                    order_by
                )


                query=query.order_by(
                    asc(order_col)
                    if ascending
                    else desc(order_col)
                )



            query=query.offset(
                (page-1)*page_size
            ).limit(
                page_size
            )



            result = await session.execute(
                query
            )


            return (
                result.scalars().all(),
                total_count
            )



    # ===============================
    # 原生SQL
    # ===============================


    async def execute_sql(
        self,
        sql:str,
        params:dict=None
    )->Any:


        async with self.session_scope() as session:


            result = await session.execute(
                text(sql),
                params or {}
            )


            # SELECT
            if result.returns_rows:

                return result.mappings().all()


            # UPDATE DELETE INSERT
            return result.rowcount



    async def execute_sql_batch(
        self,
        sql_list:List[str],
        params_list:Optional[List[dict]]=None
    )->None:


        async with self.session_scope() as session:


            for i,sql in enumerate(sql_list):


                params = (
                    params_list[i]
                    if params_list
                    else {}
                )


                await session.execute(
                    text(sql),
                    params
                )



    # ===============================
    # 手动Session
    # ===============================


    @asynccontextmanager
    async def get_session(
        self
    ):


        async with self.Session() as session:

            yield session



    # ===============================
    # 关闭连接池
    # ===============================


    async def close(
        self
    ):


        await self.engine.dispose()