from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class GroupRef(BaseModel):
    id: str

    model_config = ConfigDict(populate_by_name=True)

class GroupOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserCreate(BaseModel):
    username: str
    email: str
    display_name: str = Field(..., alias="displayName")
    groups: Optional[List[GroupRef]] = None

    model_config = ConfigDict(populate_by_name=True)

class UserUpdate(BaseModel):
    is_active: bool = Field(..., alias="isActive")

    model_config = ConfigDict(populate_by_name=True)

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    display_name: str = Field(..., alias="displayName")
    is_active: bool = Field(..., alias="isActive")
    groups: List[GroupOut] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class PagedUsers(BaseModel):
    content: List[UserOut]
    page: int
    size: int
    totalElements: int
    isLastPage: bool

    model_config = ConfigDict(populate_by_name=True)

