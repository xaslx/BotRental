from aiogram.filters import Filter
from aiogram.types import Message


class AdminProtect(Filter):

    def __init__(self):
        self.admins: list[int] = [340906161]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins