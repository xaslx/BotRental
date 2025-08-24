from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from .broker import broker

# redis_source: RedisScheduleSource = RedisScheduleSource('redis://redis:6379')
schedule: TaskiqScheduler = TaskiqScheduler(
    broker, sources=[LabelScheduleSource(broker=broker)]
)
