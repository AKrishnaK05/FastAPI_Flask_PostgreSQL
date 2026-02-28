from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.routers import auth, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize app resources on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)


@app.get("/health", tags=["health"])
def health_check():
    """Lightweight service health endpoint."""

    return {"status": "ok"}


app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
