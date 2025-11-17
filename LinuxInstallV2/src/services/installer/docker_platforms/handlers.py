import os
import subprocess
from time import sleep
from typing import Callable, Iterable, TypedDict

from .interface import OSPlatformHandler


class DebainHandler(OSPlatformHandler):

    def install_docker(
        self, pacakge_filter: Callable[[str], bool] | None = None
    ) -> bool:
        """安装docker软件包

        Returns:
            bool: 是否安装成功
        """

        if os.system("cat /etc/group | grep docker > NULL") != 0:
            os.system("sudo groupadd docker")

        os.chdir(self.pkgs_dir)

        cmd_packages = str.join(
            " ", self._get_docker_pkg_paths(self.pkgs_dir, pacakge_filter)
        )
        lastcode = os.system(f"dpkg -i {cmd_packages}")

        return lastcode == 0


class CentOSHandler(OSPlatformHandler):

    class _ShellArgs(TypedDict):
        capture_output: bool
        shell: bool
        text: bool

    def install_docker(
        self, pacakge_filter: Callable[[str], bool] | None = None
    ) -> bool:

        os.chdir(self.pkgs_dir)

        if pacakge_filter is None:
            lastcode = os.system("sudo rpm -Uvh * --force")
        else:
            cmd_packages = str.join(
                " ", self._get_docker_pkg_paths(self.pkgs_dir, pacakge_filter)
            )
            lastcode = os.system(f"sudo rpm -Uvh {cmd_packages} --force")

        return lastcode == 0 and self._wait_docker_service_started()

    def _wait_docker_service_started(self):

        shell_args: CentOSHandler._ShellArgs = {
            "capture_output": True,
            "shell": True,
            "text": True,
        }

        cmds = [
            "sudo systemctl daemon-reload",
            "sudo systemctl stop docker",
            "sudo systemctl stop docker.socket",
            "sudo systemctl enable docker",
        ]

        for cmd in cmds:
            subprocess.run(cmd, **shell_args, check=True)

        wait_count = 0
        while wait_count < 10:
            if (
                subprocess.run("sudo docker ps", **shell_args, check=False).returncode
                == 0
            ):
                print("The docker is running.")
                return True

            print(f"Waitting docker starting... the {wait_count + 1} round")

            curr_count = 0
            while curr_count < 5:
                sleep(1)
                curr_count += 1
            else:
                subprocess.run("sudo systemctl start docker", **shell_args, check=False)

            wait_count += 1

        return False

    @staticmethod
    def _get_docker_pkg_paths(
        dir_name: str, pacakge_filter: Callable[[str], bool] | None = None
    ) -> Iterable[str]:
        file_names = {name.split("_", 1)[0]: name for name in os.listdir(dir_name)}

        for package_name in OSPlatformHandler._PACKAGES:
            if pacakge_filter is None or pacakge_filter(package_name):
                yield os.path.join(".", file_names[package_name])
