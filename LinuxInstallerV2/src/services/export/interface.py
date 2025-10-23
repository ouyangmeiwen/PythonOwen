from abc import ABC, abstractmethod


class BaseExporter(ABC):

    @abstractmethod
    def run(self, project_dir: str, dist_dir: str):
        pass
