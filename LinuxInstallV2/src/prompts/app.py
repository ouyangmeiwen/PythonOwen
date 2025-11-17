import os

from configs import DbConnectionOptions, HostEnv, RuntimeEnvironment

from .connection_prompt import ConnectionSettingsPromptCreator
from .db_dirver_prompt import DbDriverPrompt
from .install_comfirm import InsallComfirmPrompt
from .location_prompt import LocationPrompt


class App:

    def __init__(self, workdir: str):
        self.workdir = workdir

    def run(self) -> tuple[RuntimeEnvironment, DbConnectionOptions]:

        env: RuntimeEnvironment | None = None
        db_options: DbConnectionOptions | None = None

        ready_install = False

        while not ready_install:
            os.system("clear")

            env = self.create_env()
            db_options = self.create_db_options(env.host_env.host_ip)

            ready_install = self.comfirm(env.target_dir, db_options)

        assert env is not None
        assert db_options is not None

        return env, db_options

    def comfirm(self, target_dir: str, options: DbConnectionOptions) -> bool:

        return InsallComfirmPrompt(
            target_dir, options.driver, options.db_host, options.db_username
        ).prompt()

    def create_db_options(self, host_ip: str) -> DbConnectionOptions:

        driver = DbDriverPrompt().prompt()

        connection_settings_prompt = ConnectionSettingsPromptCreator.create(driver)
        conn_settings = connection_settings_prompt.prompt(host_ip)

        db_options = DbConnectionOptions(
            db_host=conn_settings.host,
            db_username=conn_settings.username,
            db_name=conn_settings.dbname,
            db_passwd=conn_settings.passwd,
            db_port=conn_settings.port,
            driver=driver,
        )

        return db_options

    def create_env(self) -> RuntimeEnvironment:

        install_location = LocationPrompt().prompt()

        env = RuntimeEnvironment(
            conf_template_dir=os.path.join(self.workdir, "docker"),
            docker_image_dir=os.path.join(self.workdir, "images"),
            pkg_dir=os.path.join(self.workdir, "pkgs"),
            target_dir=install_location,
            host_env=HostEnv(),
        )

        return env
