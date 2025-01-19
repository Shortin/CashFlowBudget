import os
import subprocess
from datetime import datetime


def generate_migration():
    # Спускаемся на одну папку назад
    os.chdir(os.path.dirname(os.getcwd()))

    # Формируем имя миграции с текущей датой и временем
    migration_name = f"Migration {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    # Запуск Alembic для генерации миграции
    try:
        subprocess.run(
            ['alembic', 'revision', '--autogenerate', '-m', migration_name],
            check=True
        )

        # После генерации миграции выполняем команду git add и commit
        subprocess.run(['git', 'add', '.'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


if __name__ == '__main__':
    generate_migration()
