from fastapi import APIRouter, HTTPException
from internal import gemini_api

router = APIRouter(
    prefix="/process",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def read_items(image: str):
    return gemini_api.generate_structured_recipes(image_url=image)
