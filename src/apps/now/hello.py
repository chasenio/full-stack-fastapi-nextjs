import asyncio
import time
import typing as t
from fastapi import Depends
from fastapi import APIRouter
from datetime import datetime
from datetime import timezone
from pydantic import BaseModel

router = APIRouter()


class HelloResponse(BaseModel):
    now: str


@router.get("/hello", response_model=HelloResponse)
async def hello():
    return HelloResponse(now=datetime.now(timezone.utc).isoformat())
