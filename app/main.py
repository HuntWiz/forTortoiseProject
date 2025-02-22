import uvicorn
from fastapi import FastAPI

from app.routers import post, tag

from tortoise.contrib.fastapi import register_tortoise, RegisterTortoise

import logging


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
app.include_router(post.router)
app.include_router(tag.router)

TORTOISE_ORM = {
    "connections": {"default": "sqlite://../db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)





if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)