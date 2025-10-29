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
        try:

            if not os.path.exists(self.images_dir):
                warnings.warn("没有找到加载镜像的目录")
                return False
            print("正在加载Docker镜像...")
            for image_path in self._get_file_names(self.images_dir):
                print(f"正在加载 {os.path.basename(image_path)}...")
                result = os.system(f"sudo docker load -i {image_path}")
                if result != 0:
                        raise Exception(f"加载镜像 {os.path.basename(image_path)} 失败")
                print(f"{os.path.basename(image_path)} 加载完成")
            print("所有Docker镜像加载完成")
            return True
        except Exception as e:
            print(f"Docker镜像加载过程中发生错误: {str(e)}")
            raise

    @staticmethod
    def _get_file_names(from_dir: str) -> Iterable[str]:
        file_names = (
            os.path.join(from_dir, file)
            for file in os.listdir(from_dir)
            if os.path.basename(file).endswith(".tar")
        )
        return file_names
