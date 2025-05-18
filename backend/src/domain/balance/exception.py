from src.domain.common.exception import DomainErrorException
from dataclasses import dataclass
from fastapi import status


@dataclass(eq=False)
class BalanceException(DomainErrorException):
    ...


@dataclass(eq=False)
class NegativeBalanceError(BalanceException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Баланс не должен быть отрицательным.'


@dataclass(eq=False)
class InsufficientFundsError(BalanceException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED

    @property
    def message(self) -> str:
        return 'Недостаточно средств.'


@dataclass(eq=False)
class InvalidDepositAmountError(BalanceException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Некорректная сумма пополнения.'


@dataclass(eq=False)
class InvalidWithdrawalAmountError(BalanceException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Некорректная сумма списания.'