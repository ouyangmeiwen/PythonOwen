import dmPython


class DmVaildator:

    def test_connection(
        self, host: str, port: int, username: str, passwd: str
    ) -> tuple[bool, str | None]:

        try:
            conn = dmPython.connect(
                user=username, password=passwd, server=host, port=port,
                loginTimeout=600,connectTimeout=600,
            )
            conn.close()

            return True, None

        except Exception as e:
            if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                return False, "数据库链接超时"
            return False, str(e)
