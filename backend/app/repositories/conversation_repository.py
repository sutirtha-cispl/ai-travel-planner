"""Conversation repository."""

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Conversation)
