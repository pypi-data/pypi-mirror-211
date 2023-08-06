# type: ignore
from datetime import datetime
from typing import List, Optional, Type

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel, EmailStr, constr

from .group import GroupName, RoleName
from .questionnaire import RegistrationQandA

external_user_id: Type[str] = constr(regex=r"^auth0|[a-z0-9]{24}$")


class ExternalUserId(BaseModel):
    id: external_user_id


class GroupBase(BaseModel):
    name: GroupName
    description: Optional[str]

    class Config:
        orm_mode = True


class Group(GroupBase):
    pass


class GroupCreate(GroupBase):
    pass


class RoleBase(BaseModel):
    name: RoleName
    description: Optional[str]

    class Config:
        orm_mode = True


class Role(RoleBase):
    pass


class UserBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    affiliation: str

    class Config:
        orm_mode = True
        extra = "forbid"


class UserResponse(UserBase):
    signup_date: datetime
    external_user_id: external_user_id
    group: Optional[Group]
    roles: Optional[List[Role]]


class User(UserBase):
    id: int
    external_user_id: external_user_id
    signup_date: datetime
    group: Optional[Group]
    roles: Optional[List[Role]]


class UserCreate(UserBase):
    external_user_id: external_user_id


class UserSignUp(UserBase):
    questionnaire: RegistrationQandA
    response: Optional[str]

    class Config:
        use_enum_values = True


class Quota(BaseModel):
    quota_period: str
    quota_limit: Optional[int]
    quota_remaining: Optional[int]


class Rate(BaseModel):
    rate_period: str
    rate_limit: Optional[int]
    rate_remaining: Optional[int]


class JobLimit(BaseModel):
    quotas: List[Quota]
    rates: List[Rate]


class JobLimitType(StrEnum):
    JOB_RATE = "JOB_RATE"
    JOB_QUOTA = "JOB_QUOTA"


class ContactUs(BaseModel):
    subject: str
    email: EmailStr
    content: constr(min_length=1, max_length=500)
