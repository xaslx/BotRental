from fastapi import APIRouter, status
import psutil
from src.presentation.schemas.monitoring import MonitoringOutSchema
from src.const import MB
from src.presentation.decorators.check_role import check_role
from src.domain.user.entity import UserEntity
from dishka.integrations.fastapi import inject, FromDishka as Depends


router: APIRouter = APIRouter()


@router.get(
        '/monitoring',
        status_code=status.HTTP_200_OK,
        description='Эндпоинт для мониторинга сервера',
)
@inject
@check_role(allowed_roles=['admin'])
async def get_system_stats(
    user: Depends[UserEntity],
) -> MonitoringOutSchema:
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')


    return MonitoringOutSchema(
        cpu_usage_percent=cpu_percent,
        memory_total_mb=round(memory.total / MB, 2),
        memory_used_mb=round(memory.used / MB, 2),
        memory_percent=memory.percent,
        disk_total_mb=round(disk.total / MB, 2),
        disk_used_mb=round(disk.used / MB, 2),
        disk_percent=disk.percent,
    )