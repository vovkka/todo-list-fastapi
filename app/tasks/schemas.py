from pydantic import BaseModel


class STask(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None = None


class STaskCreate(BaseModel):
    name: str
    description: str | None = None

