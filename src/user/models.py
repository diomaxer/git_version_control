import datetime
from typing import List

from pydantic import BaseModel, Field


class UserResponseV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str


class UserAddRequestV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str


class UserStat(BaseModel):
    user_id: int
    repo_id: int
    date: datetime.date
    stargazers: int
    forks: int
    watchers: int

