import os

from configs import DbConnectionOptions, HostEnv

from .configurator_interface import ServiceConfigurator
from .connection_str import DbConnectionStrBuilderCreator
from .consts import ServicePorts
from .utils import AppSettingsModifer


class AspNetServiceConfigurator(ServiceConfigurator):
    """AspNet服务配置器"""

    def __init__(self, conf_dir: str, db_options: DbConnectionOptions) -> None:
        super().__init__(conf_dir)
        self.db_options = db_options

    @property
    def _appsettings_file(self):
        return os.path.join(
            self.conf_dir, "conf", self.service_name, "appsettings.Production.json"
        )

    def _appsetings_configure(self, appsettings):

        conn_configs: dict[str, str] = appsettings["ConnectionStrings"]

        connection_str = DbConnectionStrBuilderCreator.create(
            self.db_options.driver
        ).build(self.db_options)

        for key in conn_configs.keys():
            conn_configs[key] = connection_str

    def configure(self):
        """设置服务

        Args:
            db (DbConfigs): database的相关设置项
        """
        modifer = AppSettingsModifer()
        modifer.apply(self._appsettings_file, self._appsetings_configure)


class LcpService(AspNetServiceConfigurator):

    @property
    def service_name(self):
        return "lcp"


class RfidService(AspNetServiceConfigurator):

    @property
    def service_name(self):
        return "rfid"


class LmsService(AspNetServiceConfigurator):

    def __init__(
        self, conf_dir: str, db_options: DbConnectionOptions, env: HostEnv
    ) -> None:
        super().__init__(conf_dir, db_options)
        self.env = env

    @property
    def service_name(self):
        return "lms"

    def _appsetings_configure(self, appsettings):
        super()._appsetings_configure(appsettings)

        allow_cors_ports = (
            f"http://{self.env.host_ip}:{port}"
            for port in ["http://localhost:28010", ServicePorts.WEB_V4_SITE, ServicePorts.RFID_SITE]
        )

        if not hasattr(appsettings, "App"):
            appsettings["App"] = {}

        app: dict[str, str] = appsettings["App"]
        app["ServerRootAddress"] = (
            f"http://{self.env.host_ip}:{ServicePorts.WEB_V4_SRV}"
        )
        app["ClientRootAddress"] = (
            f"http://{self.env.host_ip}:{ServicePorts.WEB_V4_SITE}"
        )
        app["CorsOrigins"] = str.join(",", allow_cors_ports)


class GpiService(AspNetServiceConfigurator):

    @property
    def service_name(self):
        return "gpi"


class MigratorService(AspNetServiceConfigurator):
    """数据库迁移服务"""

    @property
    def service_name(self):
        return "migrator"
