from abc import ABC, abstractmethod


class Installer(ABC):
    """安装器接口"""

    @abstractmethod
    def install(self) -> bool:
        """安装"""
