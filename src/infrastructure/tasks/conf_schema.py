from pydantic import BaseModel


class TaskiqConfig(BaseModel):
    health_port: int = 8003
