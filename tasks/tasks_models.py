from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID
class TaskBase(BaseModel):
    title:Annotated[str, Field(..., min_length=1)]
    description:Annotated[str|None, Field(default=None)]
    deadline:Annotated[datetime, Field(...)]
    importance:Annotated[int, Field(..., ge=1, le=5)]
    urgency:Annotated[int, Field(..., ge=1, le=5)]

class Status(str, Enum):
    todo = "todo"
    in_progress = "in progress"
    done = "done"

class Task(TaskBase):
    id:UUID = Field(default_factory=uuid4)
    status:Status = Status.todo
    priority_score:Annotated[float, Field(...)]

class TaskRequest(TaskBase):
    pass

class TaskResponse(Task):
    pass