from pydantic import BaseModel, ConfigDict


class MonitoringOutSchema(BaseModel):
    cpu_usage_percent: float
    memory_total_mb: float
    memory_used_mb: float
    memory_percent: float
    disk_total_mb: float
    disk_used_mb: float
    disk_percent: float

    model_config = ConfigDict(from_attributes=True)
