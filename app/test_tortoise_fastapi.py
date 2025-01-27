import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport


from app.models.post import Post
from .main import app


from app.schemas import PostOut




@pytest.mark.asyncio
async def test_create_post():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post(
            "/post/posts/",
            json={
                "title":"Test",
                "content":"Test"
            }
        )
        assert response.status_code == 201

        data = response.json()
        assert set(data.keys()) == {"id", "title", "content"}
        assert isinstance(data["id"], int)
        assert data["title"] == "Test"
        assert data["content"] == "Test"

        db_post = await Post.get(id=data["id"])
        assert db_post.title == data["title"]
        assert db_post.content == data["content"]

        post_out = PostOut.from_orm(db_post)
        assert post_out.dict() == data

def test_create_post_sync():
    client = TestClient(app)
    response = client.post("post/posts/", json={"title": "Test", "content": "Test"})
    assert response.status_code == 201
