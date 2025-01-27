from pydantic import BaseModel, ValidationError, ConfigDict



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
    model_config = ConfigDict(from_attributes = True)


class CreateTag(BaseModel):
    title: str

class UpdateTag(BaseModel):
    title: str

class TagOut(TagOutBase):
    id: int
    title: str
    posts: list[PostOut] = []
    model_config = ConfigDict(from_attributes = True)



