from prompt_toolkit.shortcuts import button_dialog

from configs import Driver


class InsallComfirmPrompt:

    def __init__(
        self, target_dir: str, db_driver: Driver, db_host: str, db_username: str
    ):

        self.target_dir = target_dir
        self.db_driver = db_driver
        self.db_host = db_host
        self.db_username = db_username

    def prompt(self) -> bool:

        is_comfirm_install = button_dialog(
            title="安装确认",
            text="确认安装应用吗?\n" + self._app_info(),
            buttons=[("安装", True), ("重新填写", False), ("退出", None)],
        ).run()

        if is_comfirm_install is None:
            exit()

        return is_comfirm_install

    def _app_info(self):
        return f"""
安装路径: {self.target_dir}
数据库类型: {self.db_driver.name}
数据库地址: {self.db_host}
用户名: {self.db_username}
        """
