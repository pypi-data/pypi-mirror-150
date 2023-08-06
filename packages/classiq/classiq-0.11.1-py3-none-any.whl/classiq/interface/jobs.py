from enum import Enum
from typing import Generic, TypeVar

import pydantic
from pydantic.generics import GenericModel

T = TypeVar("T", bound=pydantic.BaseModel)
AUTH_HEADER = "Classiq-BE-Auth"


class JobID(pydantic.BaseModel):
    job_id: str


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"

    def is_final(self) -> bool:
        return self in (self.COMPLETED, self.FAILED, self.CANCELLED)


class JobDescription(GenericModel, Generic[T]):
    status: JobStatus
    description: T
