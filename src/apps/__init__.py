from fastapi import APIRouter

from .now import router as news_router

router = APIRouter()

router.include_router(news_router)
