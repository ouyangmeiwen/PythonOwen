from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from typing import Type, TypeVar, List, Optional,Any ,Tuple
from app.dbmodel.base_model import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import operators,func
from sqlalchemy import text,asc, desc
# 定义泛型 T 表示任意 SQLAlchemy 模型类
T = TypeVar("T", bound=Base) # type: ignore

class Database:
    """sqlalchemy数据仓储"""
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(self.db_url,pool_size=10, max_overflow=20)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = self.Session()
    
    def create_tables(self, models: Optional[List[Type[Base]]] = None): # type: ignore
        """创建所有数据库表，或只创建指定的表"""
        if models:
            # 提取要创建的表的名字
            tables_to_create = {model.__tablename__: Base.metadata.tables[model.__tablename__] for model in models}
            # 使用这些表名创建对应的表
            Base.metadata.create_all(bind=self.engine, tables=tables_to_create.values())
        else:
            # 创建所有表
            Base.metadata.create_all(bind=self.engine)



    def add(self, obj: T) -> None:
        """添加任意模型对象到数据库"""
        self.session.add(obj)
        self.session.commit()

    def add_bulk(self, objs: List[T]) -> None:
        """批量添加模型对象到数据库"""
        self.session.bulk_save_objects(objs)
        self.session.commit()


    def add_bulk_transaction(self, objs: List[T]) -> None:
        """
        批量插入模型对象，以事务方式处理。
        :param objs: 模型对象列表。
        """
        try:
            self.session.bulk_save_objects(objs)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


    def update(self, obj: T, **kwargs) -> T:
        """更新对象的指定字段"""
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.session.commit()
        return obj
    
    def update_bulk(self, model: Type[T], updates: List[dict]) -> None:
        """
        批量更新模型对象
        :param model: 模型类
        :param updates: 更新的字典列表，每个字典应包含主键和要更新的字段
        """
        self.session.bulk_update_mappings(model, updates)
        self.session.commit()

    def update_bulk_transaction(self, model: Type[T], updates: List[dict]) -> None:
        """
        批量更新模型对象 以事务方式处理。
        :param model: 模型类
        :param updates: 更新的字典列表，每个字典应包含主键和要更新的字段
        """
        try:
            self.session.bulk_update_mappings(model, updates)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, obj: T) -> None:
        """删除指定的对象"""
        self.session.delete(obj)
        self.session.commit()


    def delete_bulk(self, model: Type[T], ids: List[int]) -> None:
        """
        批量删除模型对象
        :param model: 模型类
        :param ids: 要删除的主键列表
        """
        self.session.query(model).filter(model.id.in_(ids)).delete(synchronize_session='fetch')
        self.session.commit()

    def delete_bulk_transaction(self, model: Type[T], ids: List[int]) -> None:
        """
        批量删除模型对象 以事务方式处理。
        :param model: 模型类
        :param ids: 要删除的主键列表
        """
        try:
            self.session.query(model).filter(model.id.in_(ids)).delete(synchronize_session='fetch')
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


    def exists(self, model: Type[T], *filters, **kwargs) -> bool:
        """
        检查记录是否存在
        :param model: 要查询的模型类。
        :param filters: 额外的过滤条件，例如 User.age > 30。
        :param kwargs: 属性名和对应值的键值对（默认为等值查询）。
        :return: 如果记录存在返回 True，否则返回 False。
        """
        query = self.session.query(model)
        
        # 添加简单等值条件
        for attr, value in kwargs.items():
            query = query.filter(getattr(model, attr) == value)
        
        # 添加复杂条件
        if filters:
            query = query.filter(*filters)
        
        # 查询是否存在
        return self.session.query(query.exists()).scalar()


    def count(self, model: Type[T], *filters, **kwargs) -> int:
        """
        统计记录总数或满足条件的记录数
        :param model: 要查询的模型类。
        :param filters: 额外的过滤条件。
        :param kwargs: 属性名和对应值的键值对（默认为等值查询）。
        :return: 记录总数。
        """
        query = self.session.query(model)
        for attr, value in kwargs.items():
            query = query.filter(getattr(model, attr) == value)
        if filters:
            query = query.filter(*filters)
        return query.count()

    def aggregate(self, model: Type[T], field: str, agg_func: str, *filters, **kwargs) -> Optional[Any]:
        """
        对指定字段进行聚合计算（如最大值、最小值、平均值、求和等）。
        :param model: 要查询的模型类。
        :param field: 要聚合的字段名。
        :param agg_func: 聚合函数（"max"、"min"、"avg"、"sum"）。
        :param filters: 额外的过滤条件。
        :param kwargs: 属性名和对应值的键值对。
        :return: 聚合结果。
        """
        query = self.session.query(getattr(func, agg_func)(getattr(model, field)))
        for attr, value in kwargs.items():
            query = query.filter(getattr(model, attr) == value)
        if filters:
            query = query.filter(*filters)
        return query.scalar()


    def get_columns(self, model: Type[T], columns: List[str], *filters, **kwargs) -> List[dict]:
        """
        查询指定列的记录
        :param model: 要查询的模型类。
        :param columns: 要返回的列名列表。
        :param filters: 额外的过滤条件。
        :param kwargs: 属性名和对应值的键值对。
        :return: 包含指定列的结果列表。
        """
        query = self.session.query(*(getattr(model, col) for col in columns))
        for attr, value in kwargs.items():
            query = query.filter(getattr(model, attr) == value)
        if filters:
            query = query.filter(*filters)
        return [dict(zip(columns, row)) for row in query.all()]


    def get_all(self, model: Type[T]) -> List[T]:
        """查询某模型类的所有记录"""
        return self.session.query(model).all()

    def get_by_id(self, model: Type[T], obj_id: int) -> Optional[T]:
        """通过 ID 查询单个记录"""
        try:
            return self.session.query(model).filter(model.id == obj_id).first()
        except NoResultFound:
            return None
    def get_by_name(self, model: Type[T], username: String) -> Optional[T]:
        """通过 ID 查询单个记录"""
        try:
            return self.session.query(model).filter(model.username == username).first()
        except NoResultFound:
            return None
        
    def first_or_default(self, model: Type[T], *filters, **kwargs) -> Optional[T]:
        """
        根据任意条件查询记录,返回单条记录。
        """
        result_lst= self.list_many(model,*filters,**kwargs)
        if result_lst and len(result_lst)>0:
            return result_lst[0]
        else:
            return None
    def list_many(self, model: Type[T], *filters, **kwargs) -> List[T]:
        """
        根据任意条件查询记录，支持复杂查询。
        :param model: 要查询的模型类。
        :param filters: 额外的过滤条件，例如 User.id > 10。
        :param kwargs: 属性名和对应值的键值对（默认为等值查询）。
        :return: 查询结果列表。
        :使用 filters 参数，接受 SQLAlchemy 表达式（and_, or_, not_ 等）
        """
        query = self.session.query(model)
        # 添加等值条件
        for attr, value in kwargs.items():
            query = query.filter(getattr(model, attr) == value)
        # 添加复杂条件
        if filters:
            query = query.filter(*filters)
        return query.all()
    
    # database = Database("your_database_url")
    # users = database.list_page_or_default(User, page=2, page_size=5, username="john_doe")
    # for user in users:
    #     print(user)

    def list_dicts_bypage(self, model: Type[T], *filters, page: int = 1, page_size: int = 10,order_by: Optional[str] = None, ascending: bool = True, **kwargs) ->  Tuple[List[T], int]:
        """
        根据任意条件查询记录，支持复杂查询，并加入分页功能。 {"total": total_count, "items": items}
        :param model: 要查询的模型类。
        :param filters: 额外的过滤条件，例如 User.id > 10。
        :param page: 页码（默认为 1）。
        :param page_size: 每页记录数（默认为 10）。
        :param order_by: 排序字段，默认为 None，即不排序。
        :param ascending: 排序方向，默认为 True（升序）。如果为 False，则按降序排序。        
        :param kwargs: 属性名和对应值的键值对（默认为等值查询）。
        :return: 查询结果列表。 {"total": total_count, "items": items}
        :使用 filters 参数，接受 SQLAlchemy 表达式（and_, or_, not_ 等）。
        """
        query = self.session.query(model)
        
        # 添加等值条件
        for attr, value in kwargs.items():
            query = query.filter(getattr(model, attr) == value)
        
        # 添加复杂条件
        if filters:
            query = query.filter(*filters)
        

        if order_by:
            if ascending:
                query = query.order_by(asc(order_by))  # 升序排序
            else:
                query = query.order_by(desc(order_by))  # 降序排序

        #统计总数
        total_count = query.count()

        # 添加分页功能
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        items =query.all()
        return items, total_count

    # database = Database("your_database_url")
    # # 查询数据
    # sql_query = "SELECT * FROM users WHERE username = :username"
    # params = {"username": "john_doe"}
    # result = database.execute_sql(sql_query, params)
    # # 打印查询结果
    # for row in result:
    #     print(row)

    # 插入数据
    # sql_insert = "INSERT INTO users (username, email) VALUES (:username, :email)"
    # params_insert = {"username": "new_user", "email": "new_user@example.com"}
    # database.execute_sql(sql_insert, params_insert)

    # # 更新数据
    # sql_update = "UPDATE users SET email = :email WHERE username = :username"
    # params_update = {"email": "updated_email@example.com", "username": "new_user"}
    # database.execute_sql(sql_update, params_update)

    # # 删除数据
    # sql_delete = "DELETE FROM users WHERE username = :username"
    # params_delete = {"username": "new_user"}
    # database.execute_sql(sql_delete, params_delete)
    def execute_sql(self, sql: str, params: dict = None) -> Any:
        """
        执行原生 SQL 语句。
        :param sql: 要执行的 SQL 查询语句。
        :param params: 可选的参数字典，适用于 SQL 查询中的占位符（例如 :param_name）。
        :return: 查询结果或影响的行数。
        """
        result = self.session.execute(text(sql), params or {})
        self.session.commit()  # 如果是修改数据的操作需要提交
        return result



    # sql_statements = [
    #     "INSERT INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')",
    #     "INSERT INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')"
    # ]

    # # 假设 db 是包含该方法的类的实例
    # db.execute_sql_batch(sql_statements)

    # sql_statements = [
    #     "INSERT INTO users (id, name, email) VALUES (:id, :name, :email)",
    #     "UPDATE users SET email = :email WHERE id = :id"
    # ]

    # params = [
    #     {"id": 1, "name": "Alice", "email": "alice@example.com"},
    #     {"id": 1, "email": "alice_new@example.com"}
    # ]

    # # 假设 db 是包含该方法的类的实例
    # db.execute_sql_batch(sql_statements, params)
    def execute_sql_batch(self, sql_list: List[str], params_list: Optional[List[dict]] = None) -> None:
        """
        批量执行原生 SQL 语句。
        :param sql_list: SQL 语句列表。
        :param params_list: 参数列表，与 SQL 列表一一对应。
        """
        try:
            for i, sql in enumerate(sql_list):
                params = params_list[i] if params_list else None
                self.session.execute(text(sql), params or {})
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e



    def begin_transaction(self):
        """开启事务"""
        self.session.begin()

    def commit_transaction(self):
        """提交事务"""
        self.session.commit()

    def rollback_transaction(self):
        """回滚事务"""
        self.session.rollback()

    def get_session(self):
        return self.Session()
    
    def close(self):
        """关闭数据库会话"""
        self.session.close()
