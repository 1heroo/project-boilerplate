from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class ItemCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=256, description='Название')
    description: str | None = Field(default=None, description='Описание')


class ItemUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=256, description='Название')
    description: str | None = Field(default=None, description='Описание')
