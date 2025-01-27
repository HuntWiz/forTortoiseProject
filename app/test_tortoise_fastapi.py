import time

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx import ASGITransport
from tortoise import Tortoise
from tortoise.contrib.test import initializer, finalizer

from app.models.post import Post
from .main import app
from app.schemas import PostOut

import pandas as pd
import dataframe_image
import psutil

tests_time = []
cpu_time = []
mem_time = []

process = psutil.Process()
cpu_usage = process.cpu_percent(interval=0.1)

def metric_score(start_cpu,start_mem, start_time, process):
    now = time.time()
    mem_end = process.memory_info().rss / 1024 / 1024
    cpu_end = psutil.cpu_percent(interval=None)
    times = now - start_time
    cpu = cpu_end - start_cpu
    mem = mem_end - start_mem
    tests_time.append(times)
    cpu_time.append(cpu)
    mem_time.append(mem)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db():
    await Tortoise.init(
        db_url="sqlite://../db.sqlite3",
        modules={'models':["app.models"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_create_post():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()
        response = await client.post(
            "/post/posts",
            json={
                "title":"Test",
                "content":"Test"
            }
        )
        metric_score(cpu_usage, mem_usage, start, process)
        assert response.status_code == 200

        data = response.json()
        assert set(data.keys()) == {"id", "title", "content"}
        assert isinstance(data["id"], int)
        assert data["title"] == "Test"
        assert data["content"] == "Test"

        db_post = await Post.get(id=data["id"])
        assert db_post.title == data["title"]
        assert db_post.content == data["content"]

        post_out = PostOut.model_validate(db_post)
        assert post_out.model_dump() == data

@pytest.mark.asyncio
async def test_all_posts():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:

        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()

        response = await client.get("post/posts",)

        metric_score(cpu_usage, mem_usage, start, process)

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_post():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post(
            "/post/posts",
            json={
                "title": "Test",
                "content": "Test"
            }

        )
        assert response.status_code == 200
        created_response = response.json()
        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()
        get_response = await client.get(
            f"/post/posts/{created_response['id']}",
        )
        metric_score(cpu_usage, mem_usage, start, process)
        assert get_response.status_code == 200

@pytest.mark.asyncio
async def test_update_post():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post(
            "/post/posts",
            json={
                "title": "Test",
                "content": "Test"
            }
        )
        assert response.status_code == 200
        created_response = response.json()

        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()

        update_response = await client.put(f"/post/posts/{created_response['id']}",
                                           json={
                                               "title": "Updated",
                                               "content": "Updated"
                                           }
                                           )

        metric_score(cpu_usage, mem_usage, start, process)

        assert update_response.status_code == 200

@pytest.mark.asyncio
async def test_delete_post():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post(
            "/post/posts",
            json={
                "title": "Test",
                "content": "Test"
            }
        )
        assert response.status_code == 200
        created_response = response.json()


        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()

        get_response = await client.delete(
            f"/post/posts/{created_response['id']}",

        )

        metric_score(cpu_usage, mem_usage, start, process)

        df = pd.DataFrame({
            "Операция": ["Чтение (1)", "Чтение(все)", "Создание", "Изменение", "Удаление"],
            "Время": [tests_time[2], tests_time[1], tests_time[0], tests_time[3], tests_time[4]],
            "Память": [mem_time[2], mem_time[1], mem_time[0], mem_time[3], mem_time[4]],

        })

        dataframe_image.export(df, "table.png", table_conversion="matplotlib", dpi=300)
        assert get_response.status_code == 200


"""@pytest.mark.asyncio
async def test_post_get_tags():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        post_response = await client.post(
            "/post/posts",
            json={
                "title": "Test",
                "content": "Test"
            }
        )
        assert post_response.status_code == 200
        post_response = post_response.json()

        tag_response = await client.post(
            '/tag/tags',
            json={
                "title": "Test",
            }
        )
        assert tag_response.status_code == 200
        tag_response = tag_response.json()

        get_response = await client.put(
            f'/tag/tags/{tag_response['id']}/{post_response['id']}',)
        await get_response.status_code == 200"""

