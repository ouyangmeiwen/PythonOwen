
from base.basedb import Database
from postsql.postsql_models import User_Postgresql
from base.libitem_model import LibItem
# PostgreSQL 连接字符串
DATABASE_URL = "postgresql+psycopg2://postgres:abc%40123@127.0.0.1:5432/postgres"
def main():
    db = Database(DATABASE_URL)
    
    # 创建表
    db.create_tables()

    # 添加用户
    new_user = User_Postgresql(username="我是中国人", email="john@example.com")
    db.add(new_user)

    # 查询所有用户
    users = db.get_all(User_Postgresql)
    print(users)

    # 根据 ID 查询用户
    user = db.get_by_name(User_Postgresql, "我是中国人")
    if user:
        print(f"User found: {user.username}")


    # 按照 ID 查询
    user_by_id = db.first_or_default(User_Postgresql, id=1)
    print(user_by_id)

    # 按照用户名查询
    user_by_name = db.first_or_default(User_Postgresql, username="我是中国人")
    print(user_by_name)

    # 按照邮箱查询
    user_by_email = db.first_or_default(User_Postgresql, email="john@example.com")
    print(user_by_email)


    # 简单查询：按单个属性查找
    users_by_name = db.list_many(User_Postgresql, username="我是中国人")
    print(users_by_name)

    # 多个属性的等值查询
    users_by_name_and_email = db.list_many(User_Postgresql, username="JohnDoe", email="john@example.com")
    print(users_by_name_and_email)

    # 复杂查询：年龄大于 25 的用户
    users_above_25 = db.list_many(User_Postgresql, User_Postgresql.username != "JohnDoe")
    print(users_above_25)

    # 复杂查询：年龄大于 20 且名字以 'J' 开头
    users_complex = db.list_many(User_Postgresql, User_Postgresql.email != "", User_Postgresql.username.like("J%"))
    print(users_complex)


    # 更新用户邮箱
    if user:
        db.update(user, email="john.doe@example.com")

    # 删除用户
    if user:
        db.delete(user)

    # 关闭连接
    db.close()

def libitemtest():
    db = Database(DATABASE_URL)
    item_list= db.list_dicts_bypage(LibItem,page=1,page_size=10)
    print(item_list["total"])
    for it in item_list["items"]:
        print(it)
    db.close()

if __name__ == "__main__":
    #main()
    libitemtest()