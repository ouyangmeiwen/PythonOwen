import os
import shutil

from .interface import BaseExporter


class ScriptExporter(BaseExporter):

    def run(self, project_dir: str, dist_dir: str):

        self._python_script(project_dir, dist_dir)

        self._shell_script(project_dir, dist_dir)

    def _shell_script(self, project_dir, dist_dir):

        src_path = os.path.join(project_dir, "shell", "setup.sh")
        dist_path = os.path.join(dist_dir, "setup.sh")

        shutil.copy(src_path, dist_path)

    def _python_script(self, project_dir, dist_dir):
        dist_path = os.path.join(dist_dir, "script")

        os.chdir(project_dir)
        os.system(
            f"""pyinstaller --onefile \
                --add-data ".venv/lib/python3.12/site-packages/dmPython.libs/libcrypto-1a20707f.so.1.1:dmPython.libs" \
                --add-data "src/configs/config.toml:configs" \
                --distpath={dist_path} src/setup.py"""
        )
