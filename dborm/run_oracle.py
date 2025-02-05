
from base.basedb import Database
from oracle.oracle_models import User_Oracle
# 配置数据库连接
DATABASE_URL = "oracle+cx_oracle://C##sa:abc123@localhost:1521/DCLHR"

def main():
    db = Database(DATABASE_URL)
    
    # 创建表
    db.create_tables()

    # 添加用户
    new_user = User_Oracle(username="我是中国人", email="john@example.com")
    db.add(new_user)

    # 查询所有用户
    users = db.get_all(User_Oracle)
    print(users)

    # 根据 ID 查询用户
    user = db.get_by_name(User_Oracle, "我是中国人")
    if user:
        print(f"User found: {user.username}")


    # 按照 ID 查询
    user_by_id = db.first_or_default(User_Oracle, id=1)
    print(user_by_id)

    # 按照用户名查询
    user_by_name = db.first_or_default(User_Oracle, username="我是中国人")
    print(user_by_name)

    # 按照邮箱查询
    user_by_email = db.first_or_default(User_Oracle, email="john@example.com")
    print(user_by_email)


    # 简单查询：按单个属性查找
    users_by_name = db.list_many(User_Oracle, username="我是中国人")
    print(users_by_name)

    # 多个属性的等值查询
    users_by_name_and_email = db.list_many(User_Oracle, username="JohnDoe", email="john@example.com")
    print(users_by_name_and_email)

    # 复杂查询：年龄大于 25 的用户
    users_above_25 = db.list_many(User_Oracle, User_Oracle.username != "JohnDoe")
    print(users_above_25)

    # 复杂查询：年龄大于 20 且名字以 'J' 开头
    users_complex = db.list_many(User_Oracle, User_Oracle.email != "", User_Oracle.username.like("J%"))
    print(users_complex)


    # 更新用户邮箱
    if user:
        db.update(user, email="john.doe@example.com")

    # 删除用户
    if user:
        db.delete(user)

    # 关闭连接
    db.close()

if __name__ == "__main__":
    main()
