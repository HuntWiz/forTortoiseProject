from fastapi import HTTPException, APIRouter
from tortoise.exceptions import DoesNotExist


from typing import List

from app.schemas import *
from app.models.post import Post
from app.models.tag import Tag

router = APIRouter(prefix='/post', tags=['post'])


@router.post("/posts/", response_model=PostOut)
async def create_post(post: CreatePost):
    post_obj = await Post.create(**post.model_dump())
    return PostOut.from_orm(post_obj)

@router.get("/posts/", response_model=List[PostOut])
async def get_posts():
    posts = await Post.all()
    return [PostOut.model_validate(post) for post in posts]

@router.get("/posts/{post_id}", response_model=PostOut)
async def get_post(post_id: int):
    try:
        post = await Post.get(id=post_id)
        return PostOut.from_orm(post)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

@router.put("/posts/{post_id}", response_model=PostOut)
async def update_post(post_id: int, post: UpdatePost):
    await Post.filter(id=post_id).update(**post.model_dump(exclude_unset=True))
    post = await Post.get(id=post_id)
    return PostOut.from_orm(post)


@router.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    deleted_count = await Post.filter(id=post_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted"}