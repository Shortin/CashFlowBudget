"""Create tables

Revision ID: da9e2d4963ac
Revises: 
Create Date: 2025-01-18 01:55:38.339748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.tables.usersTable import Role

# revision identifiers, used by Alembic.
revision: str = 'da9e2d4963ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('families',
    sa.Column('id', sa.Integer(), nullable=False, comment='id для каждой семьи'),
    sa.Column('family_name', sa.String(length=100), nullable=False, comment='Название семьи'),
    sa.Column('description', sa.Text(), nullable=True, comment='Дополнительная информация о семье'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='Дата и время создания записи о семье'),
    sa.PrimaryKeyConstraint('id'),
    schema='data',
    comment='Семейная таблица: представляет семейные группы'
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False, comment='id для каждой роли'),
    sa.Column('name', sa.String(length=20), nullable=False, comment='Название роли (например, admin, member)'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='data',
    comment='Таблица ролей пользователей'
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False, comment='id для каждого пользователя'),
    sa.Column('name', sa.String(length=100), nullable=False, comment='Имя пользователя'),
    sa.Column('birthday', sa.Date(), nullable=True, comment='Дата рождения'),
    sa.Column('family_id', sa.Integer(), nullable=True, comment='Ссылка на семейство (если имеется)'),
    sa.Column('role_id', sa.Integer(), nullable=True, comment='Ссылка на роль пользователя'),
    sa.Column('login', sa.String(length=255), nullable=False, comment='Уникальный login для входа в систему'),
    sa.Column('password_hash', sa.String(length=255), nullable=False, comment='Хэш пароля для аутентификации'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='Дата и время создания записи пользователя'),
    sa.ForeignKeyConstraint(['family_id'], ['data.families.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['data.role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login'),
    schema='data',
    comment='Таблица пользователей, содержит информацию о пользователях системы'
    )
    op.create_table('expenses',
    sa.Column('id', sa.Integer(), nullable=False, comment='id'),
    sa.Column('amount', sa.Double(), nullable=False, comment='Сумма расхода'),
    sa.Column('description', sa.Text(), nullable=True, comment='Описание расхода'),
    sa.Column('user_id', sa.Integer(), nullable=False, comment='Ссылка на пользователя, который сделал расход'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='Дата и время создания записи расхода'),
    sa.ForeignKeyConstraint(['user_id'], ['data.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='data',
    comment='Таблица расходов, представляет расходы пользователей'
    )
    op.create_table('incomes',
    sa.Column('id', sa.Integer(), nullable=False, comment='id'),
    sa.Column('amount', sa.Double(), nullable=False, comment='Сумма дохода'),
    sa.Column('description', sa.Text(), nullable=True, comment='Описание дохода'),
    sa.Column('user_id', sa.Integer(), nullable=False, comment='Ссылка на пользователя, который сделал доход'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='Дата и время создания записи дохода'),
    sa.ForeignKeyConstraint(['user_id'], ['data.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='data',
    comment='Таблица доходов, представляет доходы пользователей'
    )

    # Получаем объект соединения из Alembic
    connection = op.get_bind()

    # Создаем сессию с использованием текущего соединения
    Session = sessionmaker(bind=connection)
    session = Session()

    # Вставка данных в таблицу role через ORM
    try:
        roles = [
            Role(name='admin'),
            Role(name='user'),
            Role(name='child')
        ]
        session.add_all(roles)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('incomes', schema='data')
    op.drop_table('expenses', schema='data')
    op.drop_table('users', schema='data')
    op.drop_table('role', schema='data')
    op.drop_table('families', schema='data')
    # ### end Alembic commands ###