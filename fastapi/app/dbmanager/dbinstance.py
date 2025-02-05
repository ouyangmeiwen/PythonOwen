from app.baseinit.configinit import DATABASE_URL
from app.dbmanager.dbutils import Database
DB_INSTANCE = Database(DATABASE_URL)
