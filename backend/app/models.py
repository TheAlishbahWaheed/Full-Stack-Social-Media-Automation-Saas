from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    email:Mapped[str]=mapped_column(String(255),unique=True,index=True)
    hashed_password:Mapped[str]=mapped_column(String(255))
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now())
    social_accounts=relationship("SocialAccount",back_populates="user",cascade="all, delete-orphan")
    posts=relationship("Post",back_populates="user",cascade="all, delete-orphan")
class SocialAccount(Base):
    __tablename__="social_accounts"
    id:Mapped[int]=mapped_column(primary_key=True)
    platform:Mapped[str]=mapped_column(String(50))
    username:Mapped[str]=mapped_column(String(100))
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    user=relationship("User",back_populates="social_accounts")
class Post(Base):
    __tablename__="posts"
    id:Mapped[int]=mapped_column(primary_key=True)
    content:Mapped[str]=mapped_column(Text)
    status:Mapped[str]=mapped_column(String(30),default="draft")
    scheduled_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now())
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    user=relationship("User",back_populates="posts")
