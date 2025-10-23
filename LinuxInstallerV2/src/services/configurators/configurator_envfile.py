import os

from dotenv import dotenv_values, set_key

from configs import Driver

from .configurator_interface import ServiceConfigurator


class EnvFile(ServiceConfigurator):

    db_driver: Driver

    def __init__(self, conf_dir: str, db_driver: Driver, version: str):
        super().__init__(conf_dir)
        self.db_driver = db_driver
        self.version = version

    @property
    def service_name(self):
        return "env-file"

    def configure(self):
        env_path = os.path.join(self.conf_dir, ".env")
        env_example_path = os.path.join(self.conf_dir, ".env.example")
        env = dotenv_values(env_example_path)

        env["DATA_PATH"] = os.path.join(self.conf_dir, "data")
        env["DB_PROVIDER"] = self.db_driver.value
        env["LMS_VERSION"] = self.version

        for key, value in env.items():
            set_key(env_path, key, str(value))
