from beanie import Document, before_event, Insert, Replace, Save, Indexed
from datetime import datetime, timezone
from typing import Annotated, Optional
import bcrypt
from pydantic import BaseModel


class OTPData(BaseModel):
    password: str
    expiry_at: datetime
    
class User(Document):
    fullname: str
    email: Annotated[str, Indexed(unique=True)]
    password: str
    verified: bool = False
    OTP_data: Optional[OTPData] = None
    created_at: datetime = None
    updated_at: datetime = None

    class Settings:
        name = "users"

    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()

    @before_event(Replace, Save)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
