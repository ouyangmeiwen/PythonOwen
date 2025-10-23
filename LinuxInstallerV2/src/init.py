"""配置初始化"""

import argparse
import os

import configs
from configs import DbConnectionOptions
from configs.hosting import HostEnv
from services import configurators


class Initializer:
    """服务安装"""

    def __init__(
        self,
        work_dir: str,
        host_env: HostEnv,
        db_options: DbConnectionOptions,
    ):
        """创建服务安装器"""

        self.work_dir = work_dir
        self.host_env = host_env
        self.db_options = db_options
        self.version = configs.build_options.version

    def initialize(self):
        """初始化"""

        self._initialize_services()
        self._migrate_database()

    def _initialize_services(self):
        """配置所有服务

        Returns:
            bool: 是否成功
        """

        env: list[configurators.ServiceConfigurator] = [
            configurators.EnvFile(self.work_dir, self.db_options.driver, self.version)
        ]

        backends: list[configurators.ServiceConfigurator] = [
            configurators.LcpService(self.work_dir, self.db_options),
            configurators.RfidService(self.work_dir, self.db_options),
            configurators.LmsService(self.work_dir, self.db_options, self.host_env),
            configurators.GpiService(self.work_dir, self.db_options),
            configurators.MigratorService(self.work_dir, self.db_options),
        ]

        fronts: list[configurators.ServiceConfigurator] = [
            configurators.LmsSite(self.work_dir, self.host_env),
            configurators.RfidSite(self.work_dir, self.host_env),
        ]

        for configurator in env + backends + fronts:
            configurator.configure()

    def _migrate_database(self):
        os.chdir(self.work_dir)

        try:
            os.system("sudo docker compose down")
            os.system("sudo docker compose up migrator")
        finally:
            os.system("sudo docker compose down migrator")


def parser_workdir():
    parser = argparse.ArgumentParser(description="Invengo图书馆管理系统初始化程序.")
    parser.add_argument("-d", "--workdir", help="工作目录，包含了安装资源的目录")
    parser.add_argument("--host", help="数据库地址")
    parser.add_argument("--db", help="数据库名称", default="invengo_db")
    parser.add_argument("--user", help="数据库名称")
    parser.add_argument("--passwd", help="数据库密码")
    parser.add_argument("--port", help="数据库端口")
    parser.add_argument("--driver", help="数据库类型")
    args = parser.parse_args()
    return args


def main():

    args = parser_workdir()

    env = HostEnv()
    db_options = DbConnectionOptions(
        args.host, args.db, args.user, args.passwd, args.port, args.driver
    )

    initializer = Initializer(args.workdir, env, db_options)
    initializer.initialize()


if __name__ == "__main__":
    main()
