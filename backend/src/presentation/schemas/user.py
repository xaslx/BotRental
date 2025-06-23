from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from src.domain.user.value_object import TelegramId
from src.domain.balance.value_object import Balance
from src.domain.user.entity import Role
from datetime import datetime


class CheckCodeSchema(BaseModel):
    telegram_id: int = Field(gt=0)
    confirmation_code: int


class SendCodeSchema(BaseModel):
    telegram_id: int = Field(gt=0)


class UserOutSchema(BaseModel):
    id: int
    created_at: datetime
    telegram_id: int
    balance: int
    blocks: list

    model_config = ConfigDict(from_attributes=True)


class UserAdminViewSchema(UserOutSchema):
    is_deleted: bool
    role: Role
    
    model_config = ConfigDict(from_attributes=True)


class UpdateUserRole(BaseModel):
    role: Role


class UserBlockSchema(BaseModel):
    reason: str
    days: int


class BlockedUserOutSchema(BaseModel):
    created_at: datetime
    user_id: int
    blocked_until: datetime
    reason: str
    blocked_by: int

    model_config = ConfigDict(from_attributes=True)