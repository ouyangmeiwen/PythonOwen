"""配置初始化"""

import argparse
import os

import configs
from configs import DbConnectionOptions
from configs.hosting import HostEnv
from services import configurators

import sys
import traceback

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
        try:
            self._initialize_services()
            self._migrate_database()
        except Exception as e:
            print(f"初始化过程中发生错误: {str(e)}")
            raise

    def _initialize_services(self):
        """配置所有服务

        Returns:
            bool: 是否成功
        """
        try:
            print("正在配置服务...")
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
                try:
                    print(f"正在配置 {configurator.service_name}...")
                    configurator.configure()
                    print(f"{configurator.service_name} 配置完成")
                except Exception as e:
                    print(f"配置 {configurator.service_name} 时发生错误: {str(e)}")
                    raise
            print("所有服务配置完成")
        except Exception as e:
            print(f"服务配置过程中发生错误: {str(e)}")
            raise

    def _migrate_database(self):
        try:
            print("正在执行数据库迁移...")
            os.chdir(self.work_dir)

            try:
                print("停止现有服务...")
                os.system("sudo docker compose down")
                print("执行数据库迁移...")
                result = os.system("sudo docker compose up migrator")
                if result != 0:
                    raise Exception(f"数据库迁移命令执行失败，返回码: {result}")
            finally:
                print("清理迁移容器...")
                os.system("sudo docker compose down migrator")
            print("数据库迁移完成")
        except Exception as e:
            print(f"数据库迁移过程中发生错误: {str(e)}")
            raise

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
    try:
        args = parser_workdir()

        env = HostEnv()
        db_options = DbConnectionOptions(
            args.host, args.db, args.user, args.passwd, args.port, args.driver
        )

        initializer = Initializer(args.workdir, env, db_options)
        initializer.initialize()
    except Exception as e:
        print(f"初始化程序执行过程中发生错误: {str(e)}")
        print("错误详情:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
