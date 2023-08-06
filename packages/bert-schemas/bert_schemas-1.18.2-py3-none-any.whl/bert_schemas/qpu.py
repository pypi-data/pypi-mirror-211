import datetime
from typing import Dict, List, Optional
from fastapi_utils.enums import StrEnum
from pydantic import BaseModel, root_validator, validator


class QPUName(StrEnum):
    SMALLBERT = "SMALLBERT"
    BIGBERT = "BIGBERT"
    UNDEFINED = "UNDEFINED"

    def __str__(self):
        return str(self.value)


class QPUStatus(StrEnum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"

    def __str__(self):
        return str(self.value)


class QPUAccess(BaseModel):
    day: str
    start_time: datetime.time
    end_time: datetime.time

    class Config:
        orm_mode = True


class QPUJobType(BaseModel):
    name: str

    class Config:
        orm_mode = True


class QPU(BaseModel):
    name: QPUName
    status: QPUStatus
    qpu_access: List[QPUAccess]
    job_types: List[QPUJobType]

    @validator("job_types", pre=False)
    def job_type_names(cls, value):
        return [i.name for i in value]

    class Config:
        orm_mode = True


class QPUState(QPU):
    pending_internal_jobs: Optional[int]
    pending_external_jobs: Optional[int]


class QPUStatusUpdate(BaseModel):
    status: QPUStatus

    # @root_validator()
    # def check_status_or_hours(cls, values):
    #     if (values.get("status") is None) and (values.get("operation_hours") is None):
    #         raise ValueError("either status or operation_hours is required")
    #     return values
