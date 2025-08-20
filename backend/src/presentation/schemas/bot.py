from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field
from typing import Literal
from src.presentation.schemas.user import UserOutSchema


class CreateBotSchema(BaseModel):
    name: str
    description: str
    price: int


class UpdateBotSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class BotOutSchema(CreateBotSchema):
    id: int
    is_available: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



class BotRentalOutSchema(BaseModel):
    id: int
    user_id: int
    bot_id: int
    token: str
    rented_until: datetime
    is_active: bool


    model_config = ConfigDict(from_attributes=True)


class BotAdminOutSchema(BotOutSchema):
    rentals: list[BotRentalOutSchema] = []

    model_config = ConfigDict(from_attributes=True)


class CreateBotRentSchema(BaseModel):
    token: str
    months: Literal[1, 3, 6, 12]