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
            )
            cur = conn.cursor()
            cur.execute("select version()")
            rows = cur.fetchall()
            print("database version:", rows[0])

            cur.close()
        except Exception as e:
            return False, str(e)
        else:
            return True, None
