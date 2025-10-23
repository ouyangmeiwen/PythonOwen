import json
import os
from typing import Any, Callable


class AppSettingsModifer:
    """appsettings.json 修改器"""

    def apply(
        self,
        appsettings_file: str,
        configure_action: Callable[[Any], None],
    ):
        """配置

        Args:
            appsettings_file (str): 配置文件地址
            configure_action (Callable[[Dict[str, str]], None]): 配置回调
        """
        with open(appsettings_file, "r", encoding="utf-8") as f:
            values = json.load(f)

        configure_action(values)

        with open(appsettings_file, "w", encoding="utf-8") as f:
            json.dump(values, f, indent=2, ensure_ascii=False)


class ZipFile:
    """zip文件"""

    def unzip(self, zip_file: str, to_dir: str):
        """解压

        Args:
            zip_file (str): 压缩文件
            to_dir (str): 解压到文件夹路径
        """

        os.makedirs(to_dir, exist_ok=True)
        os.system(f"unzip -qq -o {zip_file} -d {to_dir}")
