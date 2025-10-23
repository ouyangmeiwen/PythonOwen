import os
import shutil

from prompt_toolkit import HTML, print_formatted_text

import configs
from services.export import (
    BaseExporter,
    ImageExporter,
    IsoExportert,
    ResourceExporter,
    ScriptExporter,
)


def main():

    version = configs.build_options.version
    build_number = configs.build_options.build_number

    # 1. init dist environment
    work_dir = os.getcwd()
    dist_dir = init_build_dir(work_dir)

    exporters: list[BaseExporter] = []

    # 2. export resource
    exporters.append(ResourceExporter())
    # 3. export images files
    exporters.append(ImageExporter(version))
    # 4. complie scripts
    exporters.append(ScriptExporter())
    # 5. build iso file
    exporters.append(IsoExportert(version, build_number))

    for exporter in exporters:
        exporter.run(work_dir, dist_dir)

    print_formatted_text(
        HTML("<seagreen>测试完成后可以使用 ./shell/zip_iso_file.sh 进行压缩</seagreen>")
    )


def init_build_dir(work_dir: str) -> str:
    dist_dir = os.path.join(work_dir, "dist")

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    os.makedirs(dist_dir, 0o755, exist_ok=True)

    return dist_dir


if __name__ == "__main__":
    main()
