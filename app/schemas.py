from pydantic import BaseModel
from typing import Optional
from pydantic.networks import AnyHttpUrl, EmailStr
from datetime import datetime


class LinkCreateModel(BaseModel):
    original_url: AnyHttpUrl
    custom_alias: Optional[str] = None
    expiration: Optional[datetime] = None


class LinkUpdateModel(BaseModel):
    original_url: AnyHttpUrl


class LinkDetailsModel(BaseModel):
    original_url: AnyHttpUrl
    alias: str
    click_count: int
    creation: datetime
    last_access: Optional[datetime]


class UserCreationModel(BaseModel):
    username: str
    email: EmailStr
    password: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"
