from pydantic import BaseModel, Field


class CreateItemMessage(BaseModel):
    """Contract of a message on `kafka.items_topic`. Pydantic ends at the consumer."""

    title: str = Field(min_length=1, max_length=256)
    description: str | None = None
