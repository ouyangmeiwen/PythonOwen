import os
import shutil

from configs import RuntimeEnvironment

from .interface import Installer


class DeploymentInstaller(Installer):

    def __init__(self, env: RuntimeEnvironment):

        super().__init__()
        self.template_dir = env.conf_template_dir
        self.target_dir = env.target_dir

    def install(self) -> bool:

        shutil.copytree(
            self.template_dir,
            self.target_dir,
            dirs_exist_ok=True,
        )

        if not os.access(self.target_dir, os.W_OK):
            os.system(f"sudo chmod 755 -R {self.target_dir}")

        return True
