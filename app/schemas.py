from pydantic import BaseModel, ValidationError
from tortoise.models import Model


class CreatePost(BaseModel):
    title: str
    content: str


class UpdatePost(BaseModel):
    title: str
    content: str


class TagOutBase(BaseModel):
    id: int
    title: str


class PostOut(BaseModel):

    id: int
    title: str
    content: str


    class Config:
        from_attributes = True

class CreateTag(BaseModel):
    title: str

class UpdateTag(BaseModel):
    title: str

class TagOut(TagOutBase):
    id: int
    title: str
    posts: list[PostOut] = []


    class Config:
        from_attributes = True

