"""服务配置模块抽象"""

from abc import ABC, abstractmethod


class ServiceConfigurator(ABC):
    """服务配置器"""

    def __init__(self, conf_dir: str):
        self.conf_dir = conf_dir

    @property
    @abstractmethod
    def service_name(self) -> str:
        """服务名称"""

    @abstractmethod
    def configure(self):
        """设置服务"""
