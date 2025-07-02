from taskiq_redis import RedisScheduleSource
from .broker import broker
from taskiq import TaskiqScheduler

redis_source: RedisScheduleSource = RedisScheduleSource("redis://localhost:6379/0")
schedule: TaskiqScheduler = TaskiqScheduler(broker, sources=[redis_source])