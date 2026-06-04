from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI

from app.entrypoints.exceptions_handler import register_handlers
from app.entrypoints.routers import auth, category, transaction


async def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


STARTUP_HOOKS = [
    setup_logging,
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    for hook in STARTUP_HOOKS:
        await hook()
    yield


app = FastAPI(title="aspes", lifespan=lifespan)
register_handlers(app)
app.include_router(category.router, prefix="/api/v1")
app.include_router(transaction.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
