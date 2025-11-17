from abc import ABC, abstractmethod

from configs import DbConnectionOptions, Driver


class DbConnectionStrBuilder(ABC):

    @abstractmethod
    def build(self, options: DbConnectionOptions) -> str:
        pass


class DbConnectionStrBuilderCreator:

    @staticmethod
    def create(driver: Driver) -> DbConnectionStrBuilder:

        if driver == Driver.Kingbase:
            return KingbaseConnectionStrBuilder()
        elif driver == Driver.Dm:
            return DmConnectionStrBuilder()
        elif driver == Driver.MySQL:
            return MySqlConnectionStrBuilder()
        elif driver == Driver.Vastbase:
            return VastbaseConnectionStrBuilder()
        else:
            raise Exception("Not impliment!")


class KingbaseConnectionStrBuilder(DbConnectionStrBuilder):

    # host=192.168.8.62; port=54321; username=system; password=123456; database=invengo_db; Application Name=invengo lcp; Minimum Pool Size=0; Maximum Pool Size=6; Connection Idle Lifetime=30; Timezone=+8;

    def build(self, options: DbConnectionOptions):

        opts: dict[str, str | int | bool] = {
            "minimum pool size": 0,
            "maximum pool size": 6,
            "connection idle lifetime": 30,
            "timezone": "+8",
            "Application Name": "invengo lms app",
        }

        opts["host"] = options.db_host
        opts["database"] = options.db_name
        opts["username"] = options.db_username
        opts["password"] = options.db_passwd
        opts["port"] = options.db_port

        connstr = str.join(" ", [f"{k}={v};" for k, v in opts.items()])
        return connstr


class MySqlConnectionStrBuilder(DbConnectionStrBuilder):

    # Server=mysql; port=3306; Database=invengo_db; uid=invengo_admin; pwd=123456; Convert Zero Datetime=True

    def build(self, options: DbConnectionOptions) -> str:

        opts: dict[str, str | int | bool] = {"Convert Zero Datetime": True}

        opts["server"] = options.db_host
        opts["port"] = options.db_port
        opts["database"] = options.db_name
        opts["uid"] = options.db_username
        opts["pwd"] = options.db_passwd

        connstr = str.join(" ", [f"{k}={v};" for k, v in opts.items()])
        return connstr


class DmConnectionStrBuilder(DbConnectionStrBuilder):

    # Server=192.168.8.62;User Id=pyt;PWD=Iv002161;PORT=5236;appname=dm;

    def build(self, options: DbConnectionOptions) -> str:

        opts: dict[str, str | int | bool] = {"appname": "dm"}

        opts["Server"] = options.db_host
        opts["User Id"] = options.db_username
        opts["PWD"] = options.db_passwd
        opts["PORT"] = options.db_port

        conn_str = str.join(" ", [f"{k}={v};" for k, v in opts.items()])
        return conn_str


class VastbaseConnectionStrBuilder(DbConnectionStrBuilder):

    def build(self, options: DbConnectionOptions) -> str:

        opts: dict[str, str | int | bool] = {"No Reset On Close": True}

        opts["host"] = options.db_host
        opts["database"] = options.db_name
        opts["username"] = options.db_username
        opts["password"] = options.db_passwd
        opts["port"] = options.db_port

        conn_str = str.join(" ", [f"{k}={v};" for k, v in opts.items()])
        return conn_str
