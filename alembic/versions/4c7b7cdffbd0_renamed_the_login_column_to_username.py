"""Renamed the login column to username

Revision ID: 4c7b7cdffbd0
Revises: 891a1f6a5a39
Create Date: 2025-01-20 01:05:35.227372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c7b7cdffbd0'
down_revision: Union[str, None] = '891a1f6a5a39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'users',  # Имя таблицы
        'login',  # Старое имя столбца
        new_column_name='username',  # Новое имя столбца
        existing_type=sa.String(),  # Тип данных столбца
        nullable=False,  # Столбец не может быть NULL
        existing_comment='Уникальный username пользователя',  # Существующий комментарий
        schema='data'  # Схема, если используется
    )

    op.alter_column('users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_comment='Ссылка на роль пользователя',
               schema='data')

    op.drop_constraint('users_login_key', 'users', schema='data', type_='unique')
    op.create_unique_constraint('users_username_key', 'users', ['username'], schema='data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### откат изменений, сделанных в upgrade ###

    # Переименовываем столбец 'username' обратно в 'login'
    op.alter_column(
        'users',  # Имя таблицы
        'username',  # Старое имя столбца
        new_column_name='login',  # Новое имя столбца
        existing_type=sa.String(),  # Тип данных столбца
        nullable=False,  # Столбец не может быть NULL
        existing_comment='Уникальный username пользователя',  # Существующий комментарий
        schema='data'  # Схема
    )

    # Восстанавливаем столбец 'role_id' (если это необходимо) на старые настройки
    op.alter_column(
        'users',
        'role_id',
        existing_type=sa.INTEGER(),
        nullable=False,
        existing_comment='Ссылка на роль пользователя',
        schema='data'
    )

    # Удаляем новый уникальный ограничитель для 'username'
    op.drop_constraint('users_username_key', 'users', schema='data', type_='unique')

    # Восстанавливаем старое уникальное ограничение для 'login'
    op.create_unique_constraint('users_login_key', 'users', ['login'], schema='data')

    # ### end откат ###
