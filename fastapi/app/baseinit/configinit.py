import os
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量
HOST = os.getenv("HOST", "0.0.0.0")    # Default to 127.0.0.1 if not set
print(f"HOST:{HOST}")

PORT = int(os.getenv("PORT", 8001))    # Default to 8001 if not set
print(f"PORT:{PORT}")

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:abc%40123@127.0.0.1:3306/invengodbv4")
print(f"DATABASE_URL:{DATABASE_URL}")

DATABASE_URL_ASY = os.getenv("DATABASE_URL_ASY", "mysql+aiomysql://root:abc%40123@127.0.0.1:3306/invengodbv4")
print(f"DATABASE_URL_ASY:{DATABASE_URL_ASY}")

# 从环境变量中获取秘钥和算法配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
print(f"SECRET_KEY:{SECRET_KEY}")


ALGORITHM = "HS256"  # 使用 HMAC SHA-256 算法
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "False").lower() == "true"
print(f"ENABLE_AUTH:{ENABLE_AUTH}")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
print(f"LOG_LEVEL:{LOG_LEVEL}")

EXPIRES_HOURS =int(os.getenv("EXPIRES_HOURS", 24))
print(f"EXPIRES_HOURS:{EXPIRES_HOURS}")