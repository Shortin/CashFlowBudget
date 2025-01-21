from fastapi import APIRouter
from fastapi import HTTPException

from app.crud.usersCrud import *
from app.schemas.usersSchemas import *

router = APIRouter()

# todo начать формировать нормалье запросы

# ------------------ Пользователи (Users) -------------------
#
# @router.post("/users", response_model=UserDetail, tags=["Users"])
# async def post_users(user: UserCreate):
#     """
#     Создает нового пользователя.
#
#     - **user**: Данные нового пользователя, который будет создан.
#     """
#     return await create_user_db(user=user)
#
#
# @router.get("/users/{user_id}", response_model=UserDetail, tags=["Users"])
# async def get_user_by_id(user_id: int):
#     """
#     Получает пользователя по ID.
#
#     - **user_id**: Уникальный идентификатор пользователя.
#     """
#     db_user = await get_user_db(user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @router.get("/users", response_model=list[UserDetail], tags=["Users"])
# async def get_users(skip: int = 0, limit: int = 100):
#     """
#     Получает список пользователей.
#
#     - **skip**: Количество пропущенных пользователей.
#     - **limit**: Количество пользователей, которые будут возвращены.
#     """
#     return await get_users_db(skip=skip, limit=limit)
#
#
# @router.put("/users/{user_id}", response_model=UserDetail, tags=["Users"])
# async def put_user(user_id: int, user: UserUpdate):
#     """
#     Обновляет информацию о пользователе по ID.
#
#     - **user_id**: Уникальный идентификатор пользователя.
#     - **user**: Обновленные данные пользователя.
#     """
#     db_user = await update_user_db(user_id=user_id, user=user)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @router.delete("/users/{user_id}", response_model=UserDetail, tags=["Users"])
# async def delete_user(user_id: int):
#     """
#     Удаляет пользователя по ID.
#
#     - **user_id**: Уникальный идентификатор пользователя.
#     """
#     db_user = await delete_user_db(user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# # ------------------ Семьи (Families) -------------------
#
# @router.post("/families", response_model=FamilyBase, tags=["Families"])
# async def post_family(family: FamilyBase):
#     """
#     Создает новую семью.
#
#     - **family**: Данные новой семьи, которая будет создана.
#     """
#     return await create_family_db(family=family)
#
#
# @router.get("/families/{family_id}", response_model=FamilyBase, tags=["Families"])
# async def get_family_by_id(family_id: int):
#     """
#     Получает семью по ID.
#
#     - **family_id**: Уникальный идентификатор семьи.
#     """
#     db_family = await get_family_db(family_id=family_id)
#     if db_family is None:
#         raise HTTPException(status_code=404, detail="Family not found")
#     return db_family
#
#
# @router.get("/families", response_model=list[FamilyBase], tags=["Families"])
# async def get_families(skip: int = 0, limit: int = 100):
#     """
#     Получает список семей.
#
#     - **skip**: Количество пропущенных семей.
#     - **limit**: Количество семей, которые будут возвращены.
#     """
#     return await get_families_db(skip=skip, limit=limit)
#
#
# @router.put("/families/{family_id}", response_model=FamilyBase, tags=["Families"])
# async def update_family(family_id: int, family: FamilyBase):
#     """
#     Обновляет данные семьи по ID.
#
#     - **family_id**: Уникальный идентификатор семьи.
#     - **family**: Обновленные данные семьи.
#     """
#     db_family = await update_family_db(family_id=family_id, family=family)
#     if db_family is None:
#         raise HTTPException(status_code=404, detail="Family not found")
#     return db_family
#
#
# @router.delete("/families/{family_id}", response_model=FamilyBase, tags=["Families"])
# async def delete_family(family_id: int):
#     """
#     Удаляет семью по ID.
#
#     - **family_id**: Уникальный идентификатор семьи.
#     """
#     db_family = await delete_family_db(family_id=family_id)
#     if db_family is None:
#         raise HTTPException(status_code=404, detail="Family not found")
#     return db_family
#
#
# # ------------------ Роли (Roles) -------------------
#
# @router.post("/roles", response_model=RoleBase, tags=["Roles"])
# async def post_role(role: RoleBase):
#     """
#     Создает новую роль.
#
#     - **role**: Данные новой роли, которая будет создана.
#     """
#     return await create_role_db(role=role)
#
#
# @router.get("/roles/{role_id}", response_model=RoleBase, tags=["Roles"])
# async def get_role_by_id(role_id: int):
#     """
#     Получает роль по ID.
#
#     - **role_id**: Уникальный идентификатор роли.
#     """
#     db_role = await get_role_db(role_id=role_id)
#     if db_role is None:
#         raise HTTPException(status_code=404, detail="Role not found")
#     return db_role
#
#
# @router.get("/roles", response_model=list[RoleBase], tags=["Roles"])
# async def get_roles(skip: int = 0, limit: int = 100):
#     """
#     Получает список ролей.
#
#     - **skip**: Количество пропущенных ролей.
#     - **limit**: Количество ролей, которые будут возвращены.
#     """
#     return await get_roles_db(skip=skip, limit=limit)
#
#
# @router.put("/roles/{role_id}", response_model=RoleBase, tags=["Roles"])
# async def update_role(role_id: int, role: RoleBase):
#     """
#     Обновляет информацию о роли по ID.
#
#     - **role_id**: Уникальный идентификатор роли.
#     - **role**: Обновленные данные роли.
#     """
#     db_role = await update_role_db(role_id=role_id, role=role)
#     if db_role is None:
#         raise HTTPException(status_code=404, detail="Role not found")
#     return db_role
#
#
# @router.delete("/roles/{role_id}", response_model=RoleBase, tags=["Roles"])
# async def delete_role(role_id: int):
#     """
#     Удаляет роль по ID.
#
#     - **role_id**: Уникальный идентификатор роли.
#     """
#     db_role = await delete_role_db(role_id=role_id)
#     if db_role is None:
#         raise HTTPException(status_code=404, detail="Role not found")
#     return db_role
