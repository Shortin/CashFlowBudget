import logging
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.config import DBConfig
from app.db.session import Base
from app.db.models import financeModel, usersModel  # noqa

# Загрузка переменных окружения из файла .env
load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", DBConfig().get_psycopg2_db_url())

target_metadata = Base.metadata

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_migrations_offline() -> None:
    try:
        logger.info("Запуск миграций в offline-режиме")

        # Получаем URL подключения к базе данных
        url = config.get_section(config.config_ini_section)["sqlalchemy.url"]

        # Конфигурируем Alembic для работы в оффлайн-режиме
        context.configure(
            url=url,  # Подключаемся через URL
            target_metadata=target_metadata,
            literal_binds=True,  # Используем литералы для привязки значений
            dialect_name="postgresql",  # Указываем диалект для Postgres
            include_schemas=True,  # Включаем поддержку схем
        )

        with open("migrations/versions/latest_migration.sql", "w") as f:
            # Генерируем миграции и записываем их в файл
            context.run_migrations(
                destination_path=f,  # Путь к файлу, куда записываем скрипт
            )

        logger.info("Миграции успешно сгенерированы в файл migrations/versions/latest_migration.sql")

    except Exception as e:
        logger.error(f"Ошибка при создании миграций в offline-режиме: {e}")
        raise


def run_migrations_online() -> None:
    try:
        logger.info("Запуск миграций в online-режиме")
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                include_schemas=True,  # Включаем поддержку схем
            )

            with context.begin_transaction():
                context.execute(f'create schema if not exists {target_metadata.schema};')
                context.run_migrations()
        connection.close()
        logger.info("Миграции созданы успешно")
    except Exception as e:
        logger.error(f"Ошибка при выполнении миграций в online-режиме: {e}")
        raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
