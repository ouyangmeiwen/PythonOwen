import psycopg2


class PgSQLVaildator:

    def test_connection(
        self, host: str, port: int, username: str, passwd: str, database: str
    ) -> tuple[bool, str | None]:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=passwd,
                connect_timeout=600  # 添加连接超时时间
            )
            cur = conn.cursor()
            cur.execute("select version()")
            rows = cur.fetchall()
            print("database version:", rows[0])

            cur.close()
        except Exception as e:
            if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                return False, "数据库链接超时"
            return False, str(e)
        else:
            return True, None
