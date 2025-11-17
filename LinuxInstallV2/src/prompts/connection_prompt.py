import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypedDict

from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import button_dialog

from configs import Driver, SetupExeception

from .detections.dm import DmVaildator
from .detections.mysql import MySQLVaildator
from .detections.pgsql import PgSQLVaildator


@dataclass
class ConnectionSettings:
    host: str
    dbname: str
    username: str
    passwd: str
    port: int


class ConnectionSettingsPrompt(ABC):

    @abstractmethod
    def prompt(self, default_host: str) -> ConnectionSettings:
        pass


class ConnectionSettingsPromptCreator:

    @staticmethod
    def create(driver: Driver) -> ConnectionSettingsPrompt:

        if driver == Driver.Kingbase:
            return KingbaseSettingsPrompt()
        elif driver == Driver.MySQL:
            return MySQLSettingsPrompt()
        elif driver == Driver.Dm:
            return DmSettingsPrompt()
        elif driver == Driver.Vastbase:
            return VastbaseSettingsPrompt()
        else:
            raise SetupExeception("driver error.")


class _BaseDatabaseSettingsPrompt(ConnectionSettingsPrompt):

    class DatbasePromptSession(TypedDict):
        host: PromptSession
        db: PromptSession
        username: PromptSession
        passwd: PromptSession
        port: PromptSession

    @property
    def default_port(self) -> str:
        return "54321"

    @property
    def default_db(self) -> str:
        return "invengo_db"

    @property
    def default_username(self) -> str:
        return "invengo_admin"

    def prompt(self, default_host: str, settings: ConnectionSettings | None = None):

        verify_successfully = False
        session = self._define_session()

        while not verify_successfully:

            os.system("clear")

            settings = self._show_prompt(session, default_host, settings)

            verify_successfully, error_message = self._vaildate_connection(settings)

            if not verify_successfully:
                self._show_error(
                    error_message if error_message is not None else "未知错误"
                )

        assert settings is not None
        return settings

    def _show_error(self, error_message: str):

        is_continue = button_dialog(
            title="连接是失败",
            text=HTML(
                f'<style fg="ansired">数据库连接失败，请检查数据库连接信息.</style> \n {error_message}'
            ),
            buttons=[("重新填写", True), ("退出", False)],
        ).run()

        if not is_continue:
            exit()

    def _show_prompt(
        self,
        session: DatbasePromptSession,
        LAN_ip: str,
        settings: ConnectionSettings | None,
    ) -> ConnectionSettings:

        text_host = LAN_ip if settings is None else settings.host
        text_port = self.default_port if settings is None else str(settings.port)
        text_db = self.default_db if settings is None else settings.dbname
        text_username = "" if settings is None else settings.username

        settings = ConnectionSettings(
            host=session["host"].prompt(default=text_host),
            port=int(session["port"].prompt(default=text_port)),
            dbname=session["db"].prompt(default=text_db),
            username=session["username"].prompt(default=text_username),
            passwd=session["passwd"].prompt(),
        )

        return settings

    @abstractmethod
    def _vaildate_connection(
        self, settings: ConnectionSettings
    ) -> tuple[bool, str | None]:
        pass

    def _define_session(self) -> DatbasePromptSession:

        sessions = self.DatbasePromptSession(**{})
        history_suggest = AutoSuggestFromHistory()

        sessions["host"] = PromptSession("数据库地址: ")

        sessions["port"] = PromptSession(
            "数据库端口: ",
            auto_suggest=history_suggest,
            history=InMemoryHistory([self.default_port]),
        )

        sessions["db"] = PromptSession(
            "数据库名称: ",
            auto_suggest=history_suggest,
            history=InMemoryHistory([self.default_db]),
        )

        sessions["username"] = PromptSession(
            "用户名: ",
            auto_suggest=history_suggest,
            history=InMemoryHistory([self.default_username]),
        )

        sessions["passwd"] = PromptSession("密码: ", is_password=True)

        return sessions


class KingbaseSettingsPrompt(_BaseDatabaseSettingsPrompt):

    @property
    def default_port(self):
        return "54321"

    def _vaildate_connection(
        self, settings: ConnectionSettings
    ) -> tuple[bool, str | None]:

        return PgSQLVaildator().test_connection(
            settings.host,
            settings.port,
            settings.username,
            settings.passwd,
            database="test",
        )


class MySQLSettingsPrompt(_BaseDatabaseSettingsPrompt):

    @property
    def default_port(self):
        return "3306"

    def _vaildate_connection(
        self, settings: ConnectionSettings
    ) -> tuple[bool, str | None]:

        return MySQLVaildator().test_connection(
            settings.host,
            settings.port,
            settings.username,
            settings.passwd,
            settings.dbname,
        )


class DmSettingsPrompt(_BaseDatabaseSettingsPrompt):

    @property
    def default_port(self):
        return "5236"

    @property
    def default_username(self):
        return "INVENGODBA"

    def _vaildate_connection(self, settings) -> tuple[bool, str | None]:

        success, error = DmVaildator().test_connection(
            settings.host, settings.port, settings.username, settings.passwd
        )

        if success and settings.username.upper() == "SYSDBA":
            return False, "不允许直接使用SYSDBA账号连接数据库, 请使用其他账号."

        return success, error

    def _define_session(self):

        session = super()._define_session()
        session.pop("db")
        return session

    def _show_prompt(
        self,
        session: _BaseDatabaseSettingsPrompt.DatbasePromptSession,
        LAN_ip: str,
        settings: ConnectionSettings | None,
    ):
        text_host = LAN_ip if settings is None else settings.host
        text_port = self.default_port if settings is None else str(settings.port)
        text_username = "" if settings is None else settings.username

        settings = ConnectionSettings(
            host=session["host"].prompt(default=text_host),
            port=int(session["port"].prompt(default=text_port)),
            username=session["username"].prompt(default=text_username),
            passwd=session["passwd"].prompt(),
            dbname="",
        )

        return settings


class VastbaseSettingsPrompt(_BaseDatabaseSettingsPrompt):

    @property
    def default_port(self):
        return "5432"

    def _vaildate_connection(self, settings) -> tuple[bool, str | None]:

        return PgSQLVaildator().test_connection(
            settings.host,
            settings.port,
            settings.username,
            settings.passwd,
            settings.dbname,
        )
