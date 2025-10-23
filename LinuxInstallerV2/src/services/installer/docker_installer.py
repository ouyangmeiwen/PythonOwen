import os
import re
import subprocess
from typing import TypedDict

from configs.exceptions import SetupExeception
from configs.options import RuntimeEnvironment

from .docker_platforms.factories import DockerOSPlatformFactory
from .interface import Installer


class DockerInstaller(Installer):
    """Docker 安装器"""

    # 期望的docker版本
    EXCEPT_DOCKER_VERSION = "20.10.9"

    def __init__(self, env: RuntimeEnvironment):
        self.docker_app_dir = os.path.join(env.pkg_dir, "docker")

    def install(self) -> bool:
        """安装所有依赖软件包

        Returns:
            bool: 是否全部安装成功
        """

        success, handler = DockerOSPlatformFactory.try_get_handler(self.docker_app_dir)

        if not success:
            raise SetupExeception("当前操作系统不是信创系统，或者不支持该版本")

        assert handler is not None

        if not self._has_docker():
            handler.install_docker()

        if not self._has_docker_compose():
            handler.install_docker(lambda x: x == "docker-compose-plugin")

        self._grant_docker_permission()

        return True

    def _has_docker_compose(self) -> bool:
        version_result = subprocess.run(
            "sudo docker compose version",
            text=True,
            shell=True,
            capture_output=True,
            check=False,
        )
        return version_result.returncode == 0

    def _has_docker(self) -> bool:
        version_result = subprocess.run(
            "sudo docker info", text=True, shell=True, capture_output=True, check=False
        )

        if version_result.returncode != 0:
            return False

        version = re.findall(
            r"Server Version:\s*(\d+)\.(\d+)\.(\d+)", version_result.stdout
        )[0]
        version_number = [int(x) for x in version]
        expect_version_number = [20, 10, 9]

        for curr, exp in zip(version_number, expect_version_number):
            if curr > exp:
                break
            elif curr < exp:
                return False

        return True

    _ShellArgs = TypedDict(
        "_ShellArgs",
        {"capture_output": bool, "shell": bool, "text": bool, "check": bool},
    )

    def _grant_docker_permission(self) -> bool:
        """授予docker权限"""

        shell_args: DockerInstaller._ShellArgs = {
            "capture_output": True,
            "shell": True,
            "text": True,
            "check": True,
        }

        subprocess.run("sudo usermod -aG docker $USER", **shell_args)

        return True
