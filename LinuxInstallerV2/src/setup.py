import argparse
import os

import configs
from configs import Driver
from init import Initializer
from prompts.app import App
from services import installer
from sys_ctl import SysCtl


def parser_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Invengo图书馆管理系统安装程序.")
    parser.add_argument(
        "-d",
        "--workdir",
        type=str,
        help="工作目录，包含了安装资源的目录",
        required=True,
    )
    args = parser.parse_args()
    return args


def main():
    args = parser_arguments()

    # 0: user settings
    env, db_options = App(args.workdir).run()

    # 1: install docker, import images, deploy compose files
    install_depends(env)
    # 2: initialize configuration
    configure(env, db_options)
    # 3: start services
    start(env, db_options)


def install_depends(env: configs.RuntimeEnvironment):
    installer.DockerInstaller(env).install()
    installer.DockerImageInstaller(env).install()
    installer.DeploymentInstaller(env).install()


def configure(env: configs.RuntimeEnvironment, db_options: configs.DbConnectionOptions):
    initalizer = Initializer(env.target_dir, env.host_env, db_options)
    initalizer.initialize()


def start(env: configs.RuntimeEnvironment, db_options: configs.DbConnectionOptions):
    ctl = SysCtl(env.target_dir, db_options.driver)
    ctl.restart()


def arguments_resolve_to_settings(args: argparse.Namespace):
    env = configs.RuntimeEnvironment(
        os.path.join(args.workdir, "docker"),
        os.path.join(args.workdir, "images"),
        os.path.join(args.workdir, "pkgs"),
        "/opt/invengo/lms_v4",
        configs.HostEnv(),
    )

    db_options = configs.DbConnectionOptions(
        db_host="192.168.8.62",
        db_name="invengo_db",
        db_username="invengo_admin",
        db_passwd="Iv002161",
        db_port=3306,
        driver=Driver.Dm,
    )

    return env, db_options


if __name__ == "__main__":
    main()
