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
        try:
            success, handler = DockerOSPlatformFactory.try_get_handler(self.docker_app_dir)

            if not success:
                raise SetupExeception("当前操作系统不是信创系统，或者不支持该版本")

            assert handler is not None

            if not self._has_docker():
                print("正在安装Docker...")
                if not handler.install_docker():
                    raise SetupExeception("Docker安装失败")

            if not self._has_docker_compose():
                print("正在安装Docker Compose插件...")
                if not handler.install_docker(lambda x: x == "docker-compose-plugin"):
                    raise SetupExeception("Docker Compose安装失败")

            self._grant_docker_permission()

            return True
        except Exception as e:
            print(f"Docker安装过程中发生错误: {str(e)}")
            raise

    def _has_docker_compose(self) -> bool:
        try:
            version_result = subprocess.run(
                "sudo docker compose version",
                text=True,
                shell=True,
                capture_output=True,
                check=False,
            )
            return version_result.returncode == 0
        except Exception as e:
            print(f"检查Docker Compose时发生错误: {str(e)}")
            return False

    def _has_docker(self) -> bool:
        try:
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
        except Exception as e:
            print(f"检查Docker时发生错误: {str(e)}")
            return False

    _ShellArgs = TypedDict(
        "_ShellArgs",
        {"capture_output": bool, "shell": bool, "text": bool, "check": bool},
    )

    def _grant_docker_permission(self) -> bool:
        """授予docker权限"""
        try:
            shell_args: DockerInstaller._ShellArgs = {
                "capture_output": True,
                "shell": True,
                "text": True,
                "check": True,
            }

            result = subprocess.run("sudo usermod -aG docker $USER", **shell_args)
            if result.returncode != 0:
                raise Exception(f"授予Docker权限失败: {result.stderr}")
            
            print("Docker权限已授予，可能需要重新登录才能生效")
            return True
        except Exception as e:
            print(f"授予Docker权限时发生错误: {str(e)}")
            raise