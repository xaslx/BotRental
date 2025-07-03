from taskiq_redis import RedisScheduleSource
from .broker import broker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler
from .tasks import send_system_stats


# redis_source: RedisScheduleSource = RedisScheduleSource('redis://redis:6379')
schedule: TaskiqScheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker=broker)])
