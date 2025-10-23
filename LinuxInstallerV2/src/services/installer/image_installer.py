import os
import warnings
from typing import Iterable

from configs import RuntimeEnvironment

from .interface import Installer


class DockerImageInstaller(Installer):
    """Docker镜像安装"""

    def __init__(self, env: RuntimeEnvironment):
        self.images_dir = env.docker_image_dir

    def install(self) -> bool:
        """加载镜像"""

        if not os.path.exists(self.images_dir):
            warnings.warn("没有找到加载镜像的目录")
            return False

        for image_path in self._get_file_names(self.images_dir):
            os.system(f"sudo docker load -i {image_path}")

        return True

    @staticmethod
    def _get_file_names(from_dir: str) -> Iterable[str]:
        file_names = (
            os.path.join(from_dir, file)
            for file in os.listdir(from_dir)
            if os.path.basename(file).endswith(".tar")
        )
        return file_names
