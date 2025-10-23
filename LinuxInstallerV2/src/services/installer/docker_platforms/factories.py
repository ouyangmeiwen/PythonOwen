import os
import subprocess

from .handlers import CentOSHandler, DebainHandler
from .interface import OSPlatformHandler


class DockerOSPlatformFactory:

    @staticmethod
    def try_get_handler(pkgs_dir: str) -> tuple[bool, OSPlatformHandler | None]:
        """创建安装处理器
        Arguments:
            pkgs_dir(str) : docker安装包目录

        Returns:
            DockerInstallerHandler: 安装器
            如果没有找到则返回NONE
        """

        shell_args: OSPlatformHandler.ShellArg = {
            "capture_output": True,
            "shell": True,
            "text": True,
            "check": False,
        }

        is_ubuntu = subprocess.run("sudo apt --version", **shell_args).returncode == 0

        if is_ubuntu:
            rel_pkgs_dir = os.path.join(pkgs_dir, "debain")
            return True, DebainHandler(rel_pkgs_dir)

        is_centos = subprocess.run("sudo dnf --version", **shell_args).returncode == 0

        if is_centos:
            rel_pkgs_dir = os.path.join(pkgs_dir, "centos-8")
            return True, CentOSHandler(rel_pkgs_dir)

        return False, None
