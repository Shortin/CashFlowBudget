from sqlalchemy.orm import Session

from app.db.models.usersTable import *
from app.schemas.users import *
from app.utils.crud_utils import create_entity, get_entity, get_entities, update_entity, delete_entity


# CRUD для User
def create_user_db(db: Session, user: UserCreate):
    return create_entity(
        db,
        User,
        name=user.name,
        birthday=user.birthday,
        login=user.login,
        password_hash=user.password_hash,
        family_id=user.family_id,
        role_id=user.role_id,
    )


def get_user_db(db: Session, user_id: int):
    return get_entity(db, User, user_id)


def get_users_db(db: Session, skip: int = 0, limit: int = 100):
    return get_entities(db, User, skip, limit)


def update_user_db(db: Session, user_id: int, user: UserUpdate):
    return update_entity(db, User, user_id, user.model_dump(exclude_unset=True))


def delete_user_db(db: Session, user_id: int):
    return delete_entity(db, User, user_id)


# CRUD для Family
def create_family_db(db: Session, family: FamilyBase):
    return create_entity(
        db,
        Family,
        family_name=family.family_name,
        description=family.description,
    )


def get_family_db(db: Session, family_id: int):
    return get_entity(db, Family, family_id)


def get_families_db(db: Session, skip: int = 0, limit: int = 100):
    return get_entities(db, Family, skip, limit)


def update_family_db(db: Session, family_id: int, family: FamilyBase):
    return update_entity(db, Family, family_id, family.model_dump(exclude_unset=True))


def delete_family_db(db: Session, family_id: int):
    return delete_entity(db, Family, family_id)


# CRUD для Role
def create_role_db(db: Session, role: RoleBase):
    return create_entity(db, Role, name=role.name)


def get_role_db(db: Session, role_id: int):
    return get_entity(db, Role, role_id)


def get_roles_db(db: Session, skip: int = 0, limit: int = 100):
    return get_entities(db, Role, skip, limit)


def update_role_db(db: Session, role_id: int, role: RoleBase):
    return update_entity(db, Role, role_id, role.model_dump(exclude_unset=True))


def delete_role_db(db: Session, role_id: int):
    return delete_entity(db, Role, role_id)
