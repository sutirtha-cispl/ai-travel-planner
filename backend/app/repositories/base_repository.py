"""Generic base repository providing common CRUD operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.base import Base


class BaseRepository[ModelType: Base]:
    def __init__(self, db: Session, model: type[ModelType]) -> None:
        self.db = db
        self.model = model

    def get(self, model_id: object) -> ModelType | None:
        return self.db.get(self.model, model_id)

    def list(self) -> list[ModelType]:
        result = self.db.execute(select(self.model))
        return list(result.scalars().all())

    def create(self, **values: object) -> ModelType:
        instance = self.model(**values)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
