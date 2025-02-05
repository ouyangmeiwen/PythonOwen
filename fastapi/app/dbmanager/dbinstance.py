from app.baseinit.configinit import DATABASE_URL,DATABASE_URL_ASY
from app.dbmanager.dbutils import Database
from app.dbmanager.dbutils_asy import DatabaseAsy

DB_INSTANCE = Database(DATABASE_URL)
DB_INSTANCE_ASY = DatabaseAsy(DATABASE_URL_ASY)

