from app.db.models.usersModel import User
from app.schemas.authSchemas import SUserRegister
from app.service.usersService import get_role_id_by_name


def registerNewUsers(user_data: SUserRegister):
    role_id = get_role_id_by_name(user_data.role_name)
    if role_id is None:
        raise ValueError(f"Роль с именем {user_data.role_name} не найдена")

    # if user_data.family is not None:
