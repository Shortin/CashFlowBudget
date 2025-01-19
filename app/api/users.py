from fastapi import APIRouter

from app.crud.users import *
from app.db.session import get_db
from app.schemas.users import *

router = APIRouter()

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


@router.post("/users", response_model=UserDetail)
def post_users(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_db(db=db, user=user)


@router.get("/users/{user_id}", response_model=UserDetail)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_db(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users", response_model=list[UserDetail])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users_db(db=db, skip=skip, limit=limit)


@router.put("/users/{user_id}", response_model=UserDetail)
def put_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user_db(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=UserDetail)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user_db(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ------------------ Семьи (Family) -------------------

@router.post("/families", response_model=FamilyBase)
def post_family(family: FamilyBase, db: Session = Depends(get_db)):
    return create_family_db(db=db, family=family)


@router.get("/families/{family_id}", response_model=FamilyBase)
def get_family_by_id(family_id: int, db: Session = Depends(get_db)):
    db_family = get_family_db(db=db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    return db_family


@router.get("/families", response_model=list[FamilyBase])
def get_families(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_families_db(db=db, skip=skip, limit=limit)


@router.put("/families/{family_id}", response_model=FamilyBase)
def update_family(family_id: int, family: FamilyBase, db: Session = Depends(get_db)):
    db_family = update_family_db(db=db, family_id=family_id, family=family)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    return db_family


@router.delete("/families/{family_id}", response_model=FamilyBase)
def delete_family(family_id: int, db: Session = Depends(get_db)):
    db_family = delete_family_db(db=db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    return db_family


# ------------------ Роли (Role) -------------------

@router.post("/roles", response_model=RoleBase)
def post_role(role: RoleBase, db: Session = Depends(get_db)):
    return create_role_db(db=db, role=role)


@router.get("/roles/{role_id}", response_model=RoleBase)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role_db(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.get("/roles", response_model=list[RoleBase])
def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_roles_db(db=db, skip=skip, limit=limit)


@router.put("/roles/{role_id}", response_model=RoleBase)
def update_role(role_id: int, role: RoleBase, db: Session = Depends(get_db)):
    db_role = update_role_db(db=db, role_id=role_id, role=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.delete("/roles/{role_id}", response_model=RoleBase)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = delete_role_db(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role
