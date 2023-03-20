from copy import copy
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy_utils.functions.orm import quote
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine
from aps.conf import settings
from sqlalchemy.engine.url import make_url


async def init_database(
    engine: AsyncEngine,
    overwrite: bool = False,
):
    import alembic.command
    from alembic.config import Config

    # if not database_exists(settings.SQLALCHEMY_DATABASE_URI):
    await async_create_database(engine=engine)
    # elif overwrite:
    #     pass

    config = Config("alembic.ini")
    config.attributes["configure_logger"] = False

    alembic.command.upgrade(config, "head")


async def drop_database(engine):
    from sqlalchemy.orm import close_all_sessions

    close_all_sessions()

    await async_drop_database(engine.url)


async def async_create_database(engine: AsyncEngine, encoding="utf8", template=None):
    dialect_name = engine.dialect.name
    database = engine.url.database

    print(database)

    if dialect_name == "postgresql":
        if not template:
            template = "template1"

        text = f"CREATE DATABASE {database} ENCODING '{encoding}' TEMPLATE '{template}'"

        engine = create_async_engine(
            f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/postgres",
            isolation_level="AUTOCOMMIT",
        )

        async with engine.begin() as connection:
            await connection.execute(sa.text(text))


def _set_url_database(url, database):
    if hasattr(url, "_replace"):
        ret = url._replace(database=database)
    else:
        url = copy(url)
        url.database(database)
        ret = url
    return ret


async def async_drop_database(url: sa.URL):
    url = make_url(url)
    database = url.database
    dialect_name = url.get_dialect().name
    dialect_driver = url.get_dialect().driver

    if dialect_name == "postgresql":
        url = _set_url_database(url, database="postgres")

    if dialect_name == "postgresql" and dialect_driver in ["asyncpg"]:
        engine = create_async_engine(url, isolation_level="AUTOCOMMIT")

    if dialect_name == "postgresql":
        async with engine.begin() as connection:
            version = connection.dialect.server_version_info
            pid_column = "pid" if (version >= (9, 2)) else "procpid"
            text = f"""
            SELECT pg_terminate_backend(pg_stat_activity.{pid_column})
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{database}'
            AND {pid_column} <> pg_backend_pid();"""
            await connection.execute(sa.text(text))

            text = f"DROP DATABASE {quote(connection,database)}"
            await connection.execute(sa.text(text))

    await engine.dispose()
