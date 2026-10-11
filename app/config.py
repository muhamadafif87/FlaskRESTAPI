import os
from datetime import timedelta
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

_url = os.getenv("DATABASE_URL", "")
# SQLAlchemy tidak menerima awalan "postgres://", jadi string harus di-replace dengan "postgresql://"
if _url.startswith("postgres://"):
    _url = _url.replace("postgres://", "postgresql://", 1)


class Config:
    SQLALCHEMY_DATABASE_URI = _url

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "connect_args": {
            "options": f"-c search_path={os.getenv('DB_SCHEMA', 'embegeh')},public"
        },
    }

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_EXPIRES_MINUTES", 60)))
