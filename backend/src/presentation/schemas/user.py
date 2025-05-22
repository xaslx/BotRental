from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from src.domain.user.value_object import TelegramId
from src.domain.balance.value_object import Balance



class CheckCodeSchema(BaseModel):
    telegram_id: int = Field(gt=0)
    confirmation_code: int


class SendCodeSchema(BaseModel):
    telegram_id: int = Field(gt=0)


class UserOutSchema(BaseModel):
    id: int
    created_at: datetime
    telegram_id: TelegramId
    balance: Balance
    
    model_config = ConfigDict(from_attributes=True)