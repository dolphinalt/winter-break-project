from fastapi import Depends, FastAPI

from database import create_db_and_tables
from routers import image_process, users

app = FastAPI()

app.include_router(image_process.router)
app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"health": "200 OK"}
