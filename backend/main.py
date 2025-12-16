from fastapi import Depends, FastAPI

from routers import image_process

app = FastAPI()

app.include_router(image_process.router)

@app.get("/")
async def root():
    return {"health": "200 OK"}