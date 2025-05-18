from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from src.domain.user.value_object import TelegramId
from src.domain.balance.value_object import Balance
from enum import StrEnum


class AuthTypeSchema(StrEnum):
    REGISTER = 'REGISTER'
    LOGIN = 'LOGIN'


class SendCodeSchema(BaseModel):
    telegram_id: int
    auth_type: AuthTypeSchema


class CheckCodeSchema(BaseModel):
    telegram_id: int
    confirmation_code: int


class LoginUserWithCode(CheckCodeSchema):
    ...

class RegisterUserSchema(BaseModel):
    telegram_id: int = Field(gt=0)


class UserOutSchema(BaseModel):
    id: int
    created_at: datetime
    telegram_id: TelegramId
    balance: Balance
    
    model_config = ConfigDict(from_attributes=True)