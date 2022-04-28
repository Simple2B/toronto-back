from fastapi import FastAPI, APIRouter

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.routers import api_router
from app.config import settings


def create_app() -> FastAPI:
    """Create the application instance"""
    app = FastAPI(
        title=settings.SERVER_NAME,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    root_router = APIRouter()

    @root_router.get("/", tags=["Root"])
    async def root():
        """Redirect to documentation"""
        return RedirectResponse(url="/docs")

    app.include_router(root_router)
    app.include_router(api_router)

    return app
