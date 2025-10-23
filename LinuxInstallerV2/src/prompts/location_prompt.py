import os
import os.path
from pathlib import Path
from typing import TypedDict

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.validation import ValidationError, Validator


class _LocationPromptSession(TypedDict):
    target_dir: PromptSession
    data_dir: PromptSession


class LocationPrompt:

    DEFAULT_INSTALL_PATH = "/opt/invengo/lms_v4"
    DEFAULT_DATA_PATH = "/opt/invengo/lms_v4/data"

    def __init__(self):
        target_dir = PromptSession(
            "安装目标文件夹: ",
            completer=PathCompleter(only_directories=True),
            auto_suggest=AutoSuggestFromHistory(),
            validator=_DirPathValidator(),
            history=InMemoryHistory([LocationPrompt.DEFAULT_INSTALL_PATH]),
        )

        data_dir = PromptSession(
            "数据文件夹: ",
            completer=PathCompleter(only_directories=True),
            auto_suggest=AutoSuggestFromHistory(),
            validator=_DirPathValidator(),
            history=InMemoryHistory([LocationPrompt.DEFAULT_DATA_PATH]),
        )

        self.session = _LocationPromptSession(target_dir=target_dir, data_dir=data_dir)

    def prompt(self) -> str:

        target_dir = ""
        can_pass = False

        while not can_pass:

            target_dir = self.session["target_dir"].prompt(
                default=LocationPrompt.DEFAULT_INSTALL_PATH
            )

            can_pass = self.confirm(target_dir)

            os.system(f"sudo mkdir -p {target_dir}")
            os.system(f"sudo chown $USER:$USER {target_dir}")

        return target_dir

    def confirm(self, text: str) -> bool:

        if os.path.exists(text):

            target_dir = Path(text)

            if any(target_dir.iterdir()):
                return yes_no_dialog(
                    title="确认路径", text="此文件夹夹不是空文件夹，是否覆盖安装?"
                ).run()

        return True


class _DirPathValidator(Validator):

    def validate(self, document):  # type: ignore

        text = document.text

        try:
            Path(text)
        except (OSError, ValueError):
            return ValidationError(message="这个路径不是有效的路径")

        if os.path.isfile(text):
            return ValidationError(message="这个路径不是有效的文件夹")

        return None
