from pydantic import BaseModel, Field


class Task(BaseModel):
    name: str = Field(None, title="Task name", description="optional")
    description: str = Field(..., description="Brief task description", min_length=3, max_length=50)