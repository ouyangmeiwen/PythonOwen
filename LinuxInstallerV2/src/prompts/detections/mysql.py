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
            )
            conn.close()
            return True, None
        except Exception as e:
            return False, str(e)
