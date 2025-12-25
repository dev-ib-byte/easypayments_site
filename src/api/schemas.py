from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class AccessTokenResponseSchema(BaseModel):
    user_id: Optional[UUID] = Field(...)
    email: Optional[EmailStr] = Field(default=None)
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    verify: Optional[bool] = None
    user_type: Optional[str] = Field(default=None)
    message: Optional[str] = None
