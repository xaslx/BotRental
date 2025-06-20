from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.application.use_cases.admin.users.unblock_user import UnblockUserUseCase
from src.domain.user.blocked_user import BlockedUserEntity
from src.application.use_cases.admin.users.block_user import BlockUserUseCase
from src.application.use_cases.admin.users.update_role import UpdateUserRoleUseCase
from src.application.use_cases.admin.users.delete_user import DeleteUserUseCase
from src.domain.user.entity import UserEntity
from src.presentation.schemas.user import UpdateUserRole, UserAdminViewSchema, UserBlockSchema, BlockedUserOutSchema
from src.application.use_cases.admin.users.get_users import GetAllUsersUseCase, GetUserByTelegramId
from src.presentation.decorators.check_role import check_role
from src.presentation.schemas.error import ErrorSchema
from src.presentation.schemas.success import SuccessResponse


router: APIRouter = APIRouter()


@router.get(
    '/users',
    description='Эндпоинт для получения всех пользователей',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': list[UserAdminViewSchema]},
        status.HTTP_403_FORBIDDEN: {'model': ErrorSchema, 'description': 'Permission denied.'},
    },
)
@inject
@check_role(allowed_roles=['admin', 'dev'])
async def get_all_users(
    use_case: Depends[GetAllUsersUseCase],
    user: Depends[UserEntity],
) -> list[UserAdminViewSchema] | None:
    
    users: list[UserEntity] = await use_case.execute(admin=user)
    return [UserAdminViewSchema.model_validate(user) for user in users]


@router.get(
    '/users/{telegram_id}',
    description='Эндпоинт для получения конкретного пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': UserAdminViewSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema, 'description': 'User not found'},
    },
)
@inject
@check_role(allowed_roles=['admin', 'dev'])
async def get_user_by_id(
    telegram_id: int,
    user: Depends[UserEntity],
    use_case: Depends[GetUserByTelegramId],
) -> UserAdminViewSchema | None: 

    user: UserEntity | None = await use_case.execute(telegram_id=telegram_id, admin=user)
    return UserAdminViewSchema.model_validate(user)



@router.delete(
    '/users/{telegram_id}',
    description='Эндпоинт для удаления пользователя',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            'description': 'User successfully deleted.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema, 'description': 'User not found.',
        },
        status.HTTP_403_FORBIDDEN: {
            'model': ErrorSchema, 'description': 'Permission denied.',
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
    '/users/{telegram_id}/role',
    description='Эндпоинт для изменения роли у пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Role successfully updated',
            'model': UserAdminViewSchema
        },
        status.HTTP_403_FORBIDDEN: {
            'model': ErrorSchema, 'description': 'Permission denied (e.g., trying to change your own role or a developer’s role)',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorSchema, 'description': 'User not found',
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
    
    user: UserEntity = await use_case.execute(telegram_id=telegram_id, admin=user, new_role=new_role)
    return UserAdminViewSchema.model_validate(user)


@router.post(
    '/users/{telegram_id}/block',
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
            'model': ErrorSchema,
            'description': 'Insufficient permissions to perform this action',
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
    
    block: BlockedUserEntity = await use_case.execute(telegram_id=telegram_id, block_schema=block_schema, admin=user)
    return BlockedUserOutSchema.model_validate(block)


@router.post(
    '/users/{telegram_id}/unblock',
    description='Эндпоинт для разблокировки пользователя',
    status_code=status.HTTP_200_OK,
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