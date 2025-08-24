from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from src.application.use_cases.admin.users.block_user import BlockUserUseCase
from src.application.use_cases.admin.users.delete_user import DeleteUserUseCase
from src.application.use_cases.admin.users.deposit_money import DepositMoneyForUser
from src.application.use_cases.admin.users.get_users import (
    GetAllUsersUseCase,
    GetUserByTelegramId,
)
from src.application.use_cases.admin.users.unblock_user import UnblockUserUseCase
from src.application.use_cases.admin.users.update_role import UpdateUserRoleUseCase
from src.application.use_cases.admin.users.withdraw_money import WithdrawMoneyForUser
from src.domain.user.blocked_user import BlockedUserEntity
from src.domain.user.entity import UserEntity
from src.presentation.decorators.check_role import check_role
from src.presentation.schemas.error import ErrorSchema
from src.presentation.schemas.success import SuccessResponse
from src.presentation.schemas.user import (
    BlockedUserOutSchema,
    UpdateBalance,
    UpdateUserRole,
    UserAdminViewSchema,
    UserBlockSchema,
)

router: APIRouter = APIRouter()


@router.get(
    '',
    description='Эндпоинт для получения всех пользователей',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': list[UserAdminViewSchema]},
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
    },
)
@inject
@check_role(allowed_roles=['admin', 'dev'])
async def get_all_users(
    use_case: Depends[GetAllUsersUseCase],
    user: Depends[UserEntity],
) -> list[UserAdminViewSchema] | None:
    users: list[UserEntity] = await use_case.execute(admin=user)
    return [UserAdminViewSchema.model_validate(user.to_dict()) for user in users]


@router.get(
    '/{telegram_id}',
    description='Эндпоинт для получения конкретного пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': UserAdminViewSchema},
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'User not found',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
    },
)
@inject
@check_role(allowed_roles=['admin', 'dev'])
async def get_user_by_id(
    telegram_id: int,
    user: Depends[UserEntity],
    use_case: Depends[GetUserByTelegramId],
) -> UserAdminViewSchema | None:
    user: UserEntity | None = await use_case.execute(
        telegram_id=telegram_id, admin=user
    )
    return UserAdminViewSchema.model_validate(user.to_dict())


@router.delete(
    '/{telegram_id}',
    description='Эндпоинт для удаления пользователя',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            'description': 'User successfully deleted.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'User not found.',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
    },
)
@inject
@check_role(allowed_roles=['dev'])
async def delete_user(
    telegram_id: int,
    user: Depends[UserEntity],
    use_case: Depends[DeleteUserUseCase],
) -> None:
    await use_case.execute(telegram_id=telegram_id, admin=user)


@router.patch(
    '/{telegram_id}/role',
    description='Эндпоинт для изменения роли у пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Role successfully updated',
            'model': UserAdminViewSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'User not found',
        },
    },
)
@inject
@check_role(allowed_roles=['dev'])
async def update_user_role(
    telegram_id: int,
    new_role: UpdateUserRole,
    user: Depends[UserEntity],
    use_case: Depends[UpdateUserRoleUseCase],
) -> UserAdminViewSchema:
    user: UserEntity = await use_case.execute(
        telegram_id=telegram_id, admin=user, new_role=new_role
    )
    return UserAdminViewSchema.model_validate(user.to_dict())


@router.post(
    '/{telegram_id}/block',
    description='Эндпоинт для блокировки пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': BlockedUserOutSchema,
            'description': 'User was successfully blocked',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema,
            'description': 'User with the given telegram_id not found',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorSchema,
            'description': 'Invalid block data or user is already blocked',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
    },
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def block_user(
    telegram_id: int,
    block_schema: UserBlockSchema,
    user: Depends[UserEntity],
    use_case: Depends[BlockUserUseCase],
) -> BlockedUserOutSchema:
    block: BlockedUserEntity = await use_case.execute(
        telegram_id=telegram_id, block_schema=block_schema, admin=user
    )
    return BlockedUserOutSchema.model_validate(block)


@router.post(
    '/{telegram_id}/unblock',
    description='Эндпоинт для разблокировки пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'User successfully unblocked',
            'model': SuccessResponse,
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'User does not have permission to perform this action',
            'model': ErrorSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'User with the given Telegram ID not found',
            'model': ErrorSchema,
        },
    },
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def unblock_user(
    telegram_id: int,
    user: Depends[UserEntity],
    use_case: Depends[UnblockUserUseCase],
) -> SuccessResponse:
    await use_case.execute(telegram_id=telegram_id, admin=user)
    return SuccessResponse(message='Пользователь успешно разблокирован')


@router.patch(
    '/{telegram_id}/wallet/deposit',
    description='Эндпоинт для увелечения баланса пользователя',
    status_code=status.HTTP_200_OK,
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def deposit_money_for_user(
    telegram_id: int,
    schema: UpdateBalance,
    user: Depends[UserEntity],
    use_case: Depends[DepositMoneyForUser],
) -> SuccessResponse:
    await use_case.execute(telegram_id=telegram_id, admin=user, schema=schema)
    return SuccessResponse(message='Баланс пользователя изменен.')


@router.patch(
    '/{telegram_id}/wallet/withdraw',
    description='Эндпоинт для уменьшения баланса пользователя',
    status_code=status.HTTP_200_OK,
)
@inject
@check_role(allowed_roles=['dev', 'admin'])
async def withdraw_money_for_user(
    telegram_id: int,
    schema: UpdateBalance,
    user: Depends[UserEntity],
    use_case: Depends[WithdrawMoneyForUser],
) -> SuccessResponse:
    await use_case.execute(telegram_id=telegram_id, admin=user, schema=schema)
    return SuccessResponse(message='Баланс пользователя изменен.')
