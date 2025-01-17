import logging
import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

from alembic import context
from app.db import Base
from app.db.tables import budgetTable, usersTable

# Загрузка переменных окружения из файла .env
load_dotenv()

# Строка подключения к базе данных
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def run_migrations_offline() -> None:
    try:
        url = DATABASE_URL
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )
        with context.begin_transaction():
            context.execute("CREATE SCHEMA IF NOT EXISTS data")
            logger.info("Запуск миграций в offline-режиме")
            context.run_migrations()

    except Exception as e:
        logger.error(f"Ошибка при выполнении миграций в offline-режиме: {e}")
        raise


def run_migrations_online() -> None:
    try:
        logger.info("Запуск миграций в online-режиме")
        engine = create_engine(DATABASE_URL, poolclass=pool.NullPool)
        connection = engine.connect()
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema='data'
        )
        with context.begin_transaction():
            context.execute("CREATE SCHEMA IF NOT EXISTS data")
            context.configure(
                connection=connection, target_metadata=target_metadata
            )
            context.run_migrations()
        connection.close()

    except Exception as e:
        logger.error(f"Ошибка при выполнении миграций в online-режиме: {e}")
        raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
