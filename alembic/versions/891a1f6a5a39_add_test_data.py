"""add test data

Revision ID: 891a1f6a5a39
Revises: da9e2d4963ac
Create Date: 2025-01-19 02:13:10.894043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '891a1f6a5a39'
down_revision: Union[str, None] = 'da9e2d4963ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Вставляем тестовые данные в таблицу families
    op.execute("""
        INSERT INTO data.families (family_name, description, created_at)
        VALUES 
        ('Семья Ивановых', 'Маленькая семья из 3 человек', CURRENT_TIMESTAMP),
        ('Семья Петровых', 'Большая семья с 5 детьми', CURRENT_TIMESTAMP),
        ('Семья Сидоровых', 'Средняя семья, 2 ребенка', CURRENT_TIMESTAMP);
    """)

    # Вставляем тестовые данные в таблицу users
    op.execute("""
        INSERT INTO data.users (name, birthday, family_id, role_id, login, password_hash, created_at)
        VALUES
        ('Иван Иванов', '1990-05-15', 1, 1, 'ivan', 'hashedpassword1', CURRENT_TIMESTAMP),
        ('Мария Петрова', '1985-10-22', 2, 2, 'maria', 'hashedpassword2', CURRENT_TIMESTAMP),
        ('Алексей Сидоров', '2000-12-10', 3, 3, 'alexey', 'hashedpassword3', CURRENT_TIMESTAMP);
    """)

    # Вставляем тестовые данные в таблицу expenses
    op.execute("""
        INSERT INTO data.expenses (amount, description, user_id, created_at)
        VALUES
        (500.00, 'Покупка еды', 1, CURRENT_TIMESTAMP),
        (300.00, 'Транспортные расходы', 2, CURRENT_TIMESTAMP),
        (1000.00, 'Оплата коммунальных услуг', 3, CURRENT_TIMESTAMP);
    """)

    # Вставляем тестовые данные в таблицу incomes
    op.execute("""
        INSERT INTO data.incomes (amount, description, user_id, created_at)
        VALUES
        (2000.00, 'Зарплата', 1, CURRENT_TIMESTAMP),
        (2500.00, 'Премия', 2, CURRENT_TIMESTAMP),
        (1500.00, 'Дополнительный доход', 3, CURRENT_TIMESTAMP);
    """)


def downgrade():
    # Удаляем тестовые данные, чтобы откатить изменения
    op.execute("DELETE FROM data.incomes WHERE user_id IN (1, 2, 3);")
    op.execute("DELETE FROM data.expenses WHERE user_id IN (1, 2, 3);")
    op.execute("DELETE FROM data.users WHERE id IN (1, 2, 3);")
    op.execute("DELETE FROM data.role WHERE id IN (1, 2, 3);")
    op.execute("DELETE FROM data.families WHERE id IN (1, 2, 3);")