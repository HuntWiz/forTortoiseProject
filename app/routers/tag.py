from fastapi import HTTPException, APIRouter
from tortoise.exceptions import DoesNotExist


from typing import List

from app.schemas import *
from app.models.post import Post
from app.models.tag import Tag

router = APIRouter(prefix='/tag', tags=['tag'])


@router.post("/tags/", response_model=TagOut)
async def create_tag(tag: CreateTag):
    tag_obj = await Tag.create(**tag.dict())
    return TagOut.from_orm(tag_obj)

@router.get("/tags/", response_model=List[TagOut])
async def get_tags():
    tags = await Tag.all().prefetch_related("posts")
    return [TagOut.model_validate(tag) for tag in tags]

@router.get("/tags/{tag_id}", response_model=TagOut)
async def get_tag(tag_id: int):
    try:
        tag = await Tag.get(id=tag_id).prefetch_related("posts")
        return TagOut.from_orm(tag)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Tag not found")

@router.put("/tags/{tag_id}", response_model=TagOut)
async def update_tag(tag_id: int, tag: UpdateTag):
    await Tag.filter(id=tag_id).update(**tag.dict(exclude_unset=True))
    tag = await Tag.get(id=tag_id).prefetch_related("posts")
    return TagOut.from_orm(tag)

@router.put("/tags/{tag_id}/{post_id}", response_model=TagOut)
async def post_get_tags(tag_id: int, post_id: int):
    post = await Post.get(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    tag = await Tag.get(id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await tag.posts.add(post)
    await tag.fetch_related('posts')
    return tag

@router.delete("/tags/{tag_id}")
async def delete_tag(tag_id: int):
    deleted_count = await Tag.filter(id=tag_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted"}
