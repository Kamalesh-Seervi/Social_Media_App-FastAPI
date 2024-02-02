from pydantic import BaseModel,EmailStr

from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class PostFromServer(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    class Config:
        orm_mode=True
        
        
class UserCreate(BaseModel):
    email:EmailStr
    password:str
        
class UserProfileFromServer(BaseModel):
    id:int
    email:EmailStr
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    Access_Token: str
    Token_Type: str
    
class TokenData(BaseModel):
    email_address: EmailStr