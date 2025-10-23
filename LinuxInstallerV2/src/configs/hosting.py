import socket


class HostEnv:

    _host_ip = None

    @property
    def host_ip(self) -> str:
        if self._host_ip is None:
            self._host_ip = self._resolve_current_ip()

        return self._host_ip

    @host_ip.setter
    def set_host_ip(self, val: str):
        self._host_ip = val

    @staticmethod
    def _resolve_current_ip() -> str:
        st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            st.connect(("8.8.8.8", 80))
            return st.getsockname()[0]
        except Exception:
            return "127.0.0.1"
        finally:
            st.close()
