from enum import Enum, unique


@unique
class Driver(Enum):
    Kingbase = "kingbase"
    MySQL = "mysql"
    Vastbase = "vastbase"
    Dm = "dm"
