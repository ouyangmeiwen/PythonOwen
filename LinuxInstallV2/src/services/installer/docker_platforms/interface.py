import os
from abc import ABC, abstractmethod
from typing import Callable, Iterable, TypedDict


class OSPlatformHandler(ABC):

    ShellArg = TypedDict(
        "ShellArg", {"capture_output": bool, "shell": bool, "text": bool, "check": bool}
    )

    # 需要安装的包名
    _PACKAGES = [
        "containerd.io",
        "docker-ce",
        "docker-ce-cli",
        "docker-compose-plugin",
    ]

    def __init__(self, pkgs_dir: str):
        self.pkgs_dir = pkgs_dir

    @abstractmethod
    def install_docker(
        self, pacakge_filter: Callable[[str], bool] | None = None
    ) -> bool:
        """安装docker

        Args:
            pacakge_filter (Callable[[str], bool], optional): 需要安装的包过滤器. Defaults to None.

        Returns:
            bool: 是否安装成功
        """

    @staticmethod
    def _get_docker_pkg_paths(
        dir_name: str, pacakge_filter: Callable[[str], bool] | None = None
    ) -> Iterable[str]:
        """获取docker软件包路径

        Args:
            dir_name[str]: 文件夹路径

        Returns:
            Iterable[str]: 所有路径

        Yields:
            Iterator[Iterable[str]]: 安装包路径
        """

        file_names = {name.split("_", 1)[0]: name for name in os.listdir(dir_name)}

        for package_name in OSPlatformHandler._PACKAGES:
            if pacakge_filter is None or pacakge_filter(package_name):
                yield os.path.join(".", file_names[package_name])
