import pkg_resources
import toml

from . import exceptions, options
from .db_driver import Driver
from .exceptions import SetupExeception
from .options import BuildOptions, DbConnectionOptions, HostEnv, RuntimeEnvironment

# 构建选项
build_options: BuildOptions


def _load():
    """读取配置文件"""
    global build_options

    config_path = pkg_resources.resource_filename(__name__, "config.toml")
    with open(config_path) as f:
        config = toml.load(f)

        build_options = BuildOptions(**config["app"])


_load()

__all__ = [
    "exceptions",
    "options",
    "Driver",
    "SetupExeception",
    "DbConnectionOptions",
    "HostEnv",
    "RuntimeEnvironment",
]
