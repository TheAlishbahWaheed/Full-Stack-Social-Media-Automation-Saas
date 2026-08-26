from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

PLATFORMS = {"Instagram", "Facebook", "LinkedIn", "X", "TikTok"}

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ProfileUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

class SocialCreate(BaseModel):
    platform: str
    username: str = Field(min_length=1, max_length=100)
    @field_validator("platform")
    @classmethod
    def valid_platform(cls, v: str):
        if v not in PLATFORMS: raise ValueError("Unsupported platform")
        return v
    @field_validator("username")
    @classmethod
    def clean_username(cls, v: str):
        return v.strip()

class SocialOut(SocialCreate):
    id: int
    connected: bool
    model_config = ConfigDict(from_attributes=True)

class PostCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    platform: str = "Instagram"
    scheduled_at: datetime | None = None
    @field_validator("platform")
    @classmethod
    def valid_platform(cls, v: str):
        if v not in PLATFORMS: raise ValueError("Unsupported platform")
        return v

class PostUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1, max_length=5000)
    platform: str | None = None
    scheduled_at: datetime | None = None
    status: str | None = None

class PostOut(BaseModel):
    id: int
    content: str
    platform: str
    status: str
    scheduled_at: datetime | None
    published_at: datetime | None
    created_at: datetime | None
    model_config = ConfigDict(from_attributes=True)

class Analytics(BaseModel):
    total_posts: int
    drafts: int
    scheduled: int
    published: int
    connected_accounts: int
    upcoming: list[PostOut]
