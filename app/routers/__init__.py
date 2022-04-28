from fastapi import APIRouter

from .data import router as data_router

api_router = APIRouter(prefix="/api")
api_router.include_router(data_router)
