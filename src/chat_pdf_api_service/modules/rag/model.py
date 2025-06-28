from beanie import Document, Link, Insert, Update, Replace, before_event, after_event
from datetime import datetime, timezone
from ..authentication.model import User


class Chat(Document):
    prompt: str
    ai_response: str
    recipient: Link[User]
    doc_id: str
    created_at: datetime = None
    updated_at: datetime = None

    class Settings:
        name = "chats"

    @before_event(Insert)
    def set_timestamp(self):
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    @after_event(Update, Replace)
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)
