import itertools
import os
import shutil
import subprocess

from .interface import BaseExporter


class ImageExporter(BaseExporter):
    IMAGE_REGISTRT = "harbor.dev.invengolms.com"

    LMS_IMAGE_REGISTRT = f"{IMAGE_REGISTRT}/lms"

    LMS_SITE_IMAGES = ["site/rfid", "site/core"]

    LMS_IMAGES = [
        "core",
        "lcp",
        "rfid",
        "gpi",
        "migrator/dm",
        "migrator/mysql",
        "migrator/kingbase",
        "migrator/vastbase",
    ]

    DOCKER_HUB_IMAGES = ["redis:5", "emqx:5.7.0"]

    def __init__(self, lms_version: str):
        self.lms_version = lms_version

    def run(self, project_dir: str, dist_dir: str):
        self._pull_images()
        self._export_images(dist_dir)

    def _export_images(self, dist_dir: str):
        image_dir = os.path.join(dist_dir, "images")
        shutil.rmtree(image_dir, ignore_errors=True)
        os.mkdir(image_dir, 0o755)
        os.chdir(image_dir)

        lms_image_names = [
            f"{self.LMS_IMAGE_REGISTRT}/{image}:{self.lms_version}"
            for image in self.LMS_IMAGES
        ] + [
            f"{self.LMS_IMAGE_REGISTRT}/{image}:latest"
            for image in self.LMS_SITE_IMAGES
        ]
        if os.system(f"docker save {str.join(' ', lms_image_names)} -o lms.tar ") != 0:
            raise Exception("导出LMS镜像失败")

        other_image_names = [
            f"{self.IMAGE_REGISTRT}/hub/{image_with_tag}"
            for image_with_tag in self.DOCKER_HUB_IMAGES
        ]
        if (
            os.system(f"docker save {str.join(' ', other_image_names)} -o depends.tar ")
            != 0
        ):
            raise Exception("导出依赖镜像失败")

    def _pull_images(self):
        lms_image_names = (
            f"{self.LMS_IMAGE_REGISTRT}/{image}:{self.lms_version}"
            for image in self.LMS_IMAGES
        )

        lms_site_image_names = (
            f"{self.LMS_IMAGE_REGISTRT}/{image}:latest"
            for image in self.LMS_SITE_IMAGES
        )

        other_image_names = (
            f"{self.IMAGE_REGISTRT}/hub/{image_with_tag}"
            for image_with_tag in self.DOCKER_HUB_IMAGES
        )

        image_names = itertools.chain(
            lms_image_names, lms_site_image_names, other_image_names
        )

        # for image_name in image_names:
        #     os.system(f"docker pull {image_name}")
        for image_name in image_names:
            # 判断镜像是否已存在
            result = subprocess.run(
                ["docker", "image", "inspect", image_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if result.returncode == 0:
                print(f"✅ Image already exists, skip: {image_name}")
            else:
                print(f"⬇️ Pulling image: {image_name}")
                os.system(f"docker pull {image_name}")
