import pymysql
import pymysql.cursors


class MySQLVaildator:

    def test_connection(
        self, host: str, port: int, username: str, passwd: str, db: str
    ) -> tuple[bool, str | None]:

        try:
            conn = pymysql.connect(
                host=host,
                user=username,
                password=passwd,
                database=db,
                port=port,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=600,        # 连接超时时间（秒）
                read_timeout=600,           # 读取超时时间（秒）
                write_timeout=600           # 写入超时时间（秒）
            )
            conn.close()
            return True, None
        except Exception as e:
            if "timed out" in str(e).lower():
                return False, "数据库链接超时"
            return False, str(e)
