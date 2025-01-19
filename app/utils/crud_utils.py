from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def create_entity(db: Session, entity_class, **kwargs):
    """Создаёт новую запись для указанного класса сущности."""
    entity = entity_class(**kwargs)
    try:
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity
    except IntegrityError as e:
        db.rollback()
        raise e


def get_entity(db: Session, entity_class, entity_id: int):
    """Получает запись по ID."""
    return db.query(entity_class).filter_by(id=entity_id).first()


def get_entities(db: Session, entity_class, skip: int = 0, limit: int = 100):
    """Получает список записей с пропуском и ограничением."""
    return db.query(entity_class).offset(skip).limit(limit).all()


def update_entity(db: Session, entity_class, entity_id: int, update_data: dict):
    """Обновляет запись по ID."""
    entity = db.query(entity_class).filter_by(id=entity_id).first()
    if entity:
        for key, value in update_data.items():
            setattr(entity, key, value)
        db.commit()
        db.refresh(entity)
        return entity
    return None


def delete_entity(db: Session, entity_class, entity_id: int):
    """Удаляет запись по ID."""
    entity = db.query(entity_class).filter_by(id=entity_id).first()
    if entity:
        db.delete(entity)
        db.commit()
        return entity
    return None
