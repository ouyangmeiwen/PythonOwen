import dmPython


class DmVaildator:

    def test_connection(
        self, host: str, port: int, username: str, passwd: str
    ) -> tuple[bool, str | None]:

        try:
            conn = dmPython.connect(
                user=username, password=passwd, server=host, port=port
            )
            conn.close()

            return True, None

        except Exception as e:
            return False, str(e)
