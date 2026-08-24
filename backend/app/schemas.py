from datetime import datetime
from pydantic import BaseModel,ConfigDict,EmailStr,Field
class UserCreate(BaseModel):
    name:str=Field(min_length=2,max_length=100); email:EmailStr; password:str=Field(min_length=6,max_length=100)
class LoginRequest(BaseModel): email:EmailStr; password:str
class UserOut(BaseModel):
    id:int; name:str; email:EmailStr; model_config=ConfigDict(from_attributes=True)
class Token(BaseModel): access_token:str; token_type:str="bearer"; user:UserOut
class ProfileUpdate(BaseModel): name:str=Field(min_length=2,max_length=100)
class SocialCreate(BaseModel): platform:str=Field(min_length=2,max_length=50); username:str=Field(min_length=1,max_length=100)
class SocialOut(SocialCreate): id:int; model_config=ConfigDict(from_attributes=True)
class PostCreate(BaseModel): content:str=Field(min_length=1,max_length=5000); scheduled_at:datetime|None=None
class PostUpdate(BaseModel): content:str|None=Field(default=None,min_length=1,max_length=5000); scheduled_at:datetime|None=None
class PostOut(BaseModel):
    id:int; content:str; status:str; scheduled_at:datetime|None; model_config=ConfigDict(from_attributes=True)
