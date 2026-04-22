
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise_conf import TORTOISE_ORM

app = FastAPI(title="Jemo Admin API")

@app.get("/")
async def read_root():
    return {"message": "Welcome to Jemo Admin FastAPI Backend with Tortoise ORM!"}

# Database Configuration

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
