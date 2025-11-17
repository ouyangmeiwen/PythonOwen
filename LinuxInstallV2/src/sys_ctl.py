import os

from configs import Driver


class SysCtl:

    work_dir: str
    driver: Driver

    def __init__(self, work_dir: str, driver: Driver):
        self.work_dir = work_dir
        self.driver = driver

    def start(self):
        os.chdir(self.work_dir)
        os.system("sudo docker compose up -d")

    def stop(self):
        os.chdir(self.work_dir)
        os.system("sudo docker compose down")

    def restart(self):
        self.stop()
        self.start()
