from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from app.db.session import get_sessions


async def create_entity(entity_class, **kwargs):
    """Создаёт новую запись для указанного класса сущности."""
    entity = entity_class(**kwargs)
    async with get_sessions() as session:
        try:
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity
        except IntegrityError as e:
            await session.rollback()
            raise e


async def get_entity(entity_class, entity_id: int):
    """Получает запись по ID."""
    async with get_sessions() as session:
        result = await session.execute(select(entity_class).filter_by(id=entity_id))
        return result.scalars().first()


async def get_entities(entity_class, skip: int = 0, limit: int = 100):
    """Получает список записей с пропуском и ограничением."""
    async with get_sessions() as session:
        result = await session.execute(select(entity_class).offset(skip).limit(limit))
        return result.scalars().all()


async def update_entity(entity_class, entity_id: int, update_data: dict):
    """Обновляет запись по ID."""
    # Получаем сущность по ID
    async with get_sessions() as session:
        result = await session.execute(select(entity_class).filter_by(id=entity_id))
        entity = result.scalars().first()
        if entity:
            for key, value in update_data.items():
                setattr(entity, key, value)
            await session.commit()
            await session.refresh(entity)
            return entity
        return None


async def delete_entity(entity_class, entity_id: int):
    """Удаляет запись по ID."""
    async with get_sessions() as session:
        result = await session.execute(select(entity_class).filter_by(id=entity_id))
        entity = result.scalars().first()
        if entity:
            await session.delete(entity)
            await session.commit()
            return entity
        return None
