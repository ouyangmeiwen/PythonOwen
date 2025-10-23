import base64
import os
import shutil
from datetime import datetime

from .interface import BaseExporter


class IsoExportert(BaseExporter):

    def __init__(self, version: str, build_number: int):
        self.version = version
        self.build_number = build_number

    def run(self, project_dir: str, dist_dir: str):

        file_version = f"{self.version}.{self.build_number}".replace(".", "_")
        file_name = f"lms_aarch64_{file_version}.iso"

        os.system(f"genisoimage -o {file_name} -r -J {dist_dir}")

        shutil.rmtree(dist_dir)
        os.mkdir(dist_dir)

        shutil.move(
            os.path.join(project_dir, file_name), os.path.join(dist_dir, file_name)
        )

    @staticmethod
    def _encode_version(version: str) -> str:
        version_bytes = version.encode("utf-8")
        return base64.b64encode(version_bytes).decode("utf-8")

    @property
    def _generate_build_number(self) -> str:
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        diff = now - midnight

        current_day_seconds = int(diff.total_seconds())
        return str(current_day_seconds).zfill(5)
