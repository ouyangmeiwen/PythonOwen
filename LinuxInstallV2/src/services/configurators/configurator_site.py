import os
from abc import abstractmethod
from typing import Dict

from configs import HostEnv

from .configurator_interface import ServiceConfigurator
from .consts import ServicePorts
from .utils import AppSettingsModifer


class AngurlarConfigurator(ServiceConfigurator):
    """Angurlar前端配置器"""

    @property
    def _appsettings_file(self):
        return os.path.join(
            self.conf_dir, "conf", self.service_name, "appconfig.production.json"
        )

    @abstractmethod
    def _appsetings_configure(self, appsettings):
        pass

    def configure(self):
        """设置服务

        Args:
            db (DbConfigs): database的相关设置项
        """
        modifer = AppSettingsModifer()
        modifer.apply(self._appsettings_file, self._appsetings_configure)


class LmsSite(AngurlarConfigurator):
    """WEBv4"""

    def __init__(self, conf_dir: str, env: HostEnv):
        super().__init__(conf_dir)
        self.env = env

    @property
    def service_name(self):
        return "lms-site"

    def _appsetings_configure(self, appsettings: Dict[str, str]):
        # 前端访问自身地址
        appsettings["appBaseUrl"] = (
            f"http://{self.env.host_ip}:{ServicePorts.WEB_V4_SITE}"
        )
        # 前端访问呢后端地址
        appsettings["remoteServiceBaseUrl"] = (
            f"http://{self.env.host_ip}:{ServicePorts.WEB_V4_SRV}"
        )


class RfidSite(AngurlarConfigurator):
    """Rfid Site configurator"""

    def __init__(self, conf_dir: str, env: HostEnv):
        super().__init__(conf_dir)
        self.env = env

    @property
    def service_name(slef):
        return "rfid-site"

    def _appsetings_configure(self, appsettings):
        appsettings["appBaseUrl"] = (
            f"http://{self.env.host_ip}:{ServicePorts.RFID_SITE}"
        )
        appsettings["remoteServiceBaseUrl"] = (
            f"http://{self.env.host_ip}:{ServicePorts.WEB_V4_SRV}"
        )
