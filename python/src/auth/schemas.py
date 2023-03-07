from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class UserSchema(BaseModel):
    id : Optional[int] = None
    email : Optional[str] = None
    password : Optional[str] = None

    class Config:
        orm_mode = True
        

class RequestUser(BaseModel):
    parameter : UserSchema = Field(...)

class Response(BaseModel):
    code : str
    status : str
    message : str
    result : Optional[T]