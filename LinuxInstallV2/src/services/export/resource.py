import os
import os.path as osp
import shutil

from .interface import BaseExporter

DOCKER_COMPOSE_RESOURCE = "docker"
SOFTWARE_RESOURCE = "pkgs"


class ResourceExporter(BaseExporter):

    def run(self, project_dir: str, dist_dir: str):

        self.project_dir = project_dir
        self.dist_dir = dist_dir

        self._copy_docker_compose()
        self._copy_depend_software()

    def _copy_docker_compose(self):
        src = osp.join(self.project_dir, DOCKER_COMPOSE_RESOURCE)
        dist = osp.join(self.dist_dir, DOCKER_COMPOSE_RESOURCE)

        if osp.exists(dist):
            os.removedirs(dist)

        shutil.copytree(src, dist)

    def _copy_depend_software(self):
        src = osp.join(self.project_dir, SOFTWARE_RESOURCE)
        dist = osp.join(self.dist_dir, SOFTWARE_RESOURCE)

        if osp.exists(dist):
            os.removedirs(dist)

        shutil.copytree(src, dist)
