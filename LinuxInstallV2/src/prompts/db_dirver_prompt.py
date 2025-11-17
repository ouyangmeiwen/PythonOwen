from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style

from configs import Driver


class DbDriverPrompt:

    _style = Style.from_dict(
        {
            "dialog frame.label": "bg:#ffffff #000000",
            "dialog.body": "bg:#ffffff #000000",
        }
    )

    def prompt(self) -> Driver:

        selected_driver = radiolist_dialog(
            title="数据库选择",
            text="当前环境使用什么数据库?",
            values=[
                (Driver.Kingbase, "1. kingbaseES (人大金仓)"),
                (Driver.MySQL, "2. MySQL"),
                (Driver.Dm, "3. 达梦数据库"),
                (Driver.Vastbase, "4. vastbase (海量数据库)"),
            ],
            style=self._style,
            ok_text="确认",
            cancel_text="退出",
            default=Driver.Kingbase,
        ).run()

        if selected_driver is None:
            exit()

        return selected_driver
