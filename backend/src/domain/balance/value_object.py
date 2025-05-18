from dataclasses import dataclass
from src.domain.common.value_object import BaseValueObject
from src.domain.balance.exception import InsufficientFundsError


@dataclass(frozen=True)
class Balance(BaseValueObject):

    def validate(self):
        if not isinstance(self.value, int):
            raise ValueError('Баланс должен быть в виде целого числа')
        
    def add(self, amount: int) -> 'Balance':

        return Balance(self.value + amount)

    def subtract(self, amount: int) -> 'Balance':

        if self.value < amount:
            raise InsufficientFundsError()
        return Balance(self.value - amount)
    
    def to_raw(self):
        return self.value
    
    def __eq__(self, other: 'Balance') -> bool:
        if not isinstance(other, Balance):
            return False
        return self.value == other.value