from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserRead(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

