from dataclasses import dataclass

from configs.hosting import HostEnv

from .db_driver import Driver


@dataclass
class DbConnectionOptions:
    """Db设置"""

    db_host: str
    db_name: str
    db_username: str
    db_passwd: str
    db_port: int
    driver: Driver


@dataclass
class RuntimeEnvironment:
    """服务安装选项

    conf_template_dir (str): 配置模板文件夹
    pkg_dir (str): 安装包文件夹
    target_dir (str): 安装目标地址
    host_env (HostEnv): 服务环境
    """

    conf_template_dir: str
    docker_image_dir: str
    pkg_dir: str
    target_dir: str
    host_env: HostEnv


@dataclass
class BuildOptions:
    version: str
    build_number: int
