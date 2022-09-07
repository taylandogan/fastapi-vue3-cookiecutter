from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.base import settings as settings


def get_db_url(read_replica: bool = False) -> str:
    base_dsn = "postgresql://{user}:{password}@{host}:{port}/{name}".format(
        user=settings.DATABASE_USERNAME,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        name=settings.DATABASE_NAME,
    )

    if settings.DATABASE_SSL == "disable":
        return base_dsn

    ssl_mode = "prefer"
    if settings.DATABASE_SSL:
        ssl_mode = "verify-full"

    return "{base_dsn}?sslmode={ssl_mode}".format(
        base_dsn=base_dsn,
        ssl_mode=ssl_mode,
    )


engine = create_engine(
    get_db_url(),
    pool_size=settings.DATABASE_POOL_SIZE,
    pool_recycle=settings.DATABASE_POOL_RECYCLE_TTL,
    pool_pre_ping=True,
    max_overflow=settings.DATABASE_POOL_MAX_OVERFLOW,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
